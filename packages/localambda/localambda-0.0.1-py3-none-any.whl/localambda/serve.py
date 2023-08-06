"""
This file enables serving of select AWS resources locally through AWS SAM
"""
from contextlib import closing
import json
import os
import shutil
import socket
from subprocess import call, Popen, PIPE, STDOUT
import sys
from threading import Thread
import time
from typing import List

import boto3
import redis

from .decorators import threadify
from .localogger import LocaLogger
from . import LOLA_REDIS_LIST_NAME


r = redis.Redis('127.0.0.1', socket_connect_timeout=2)
logger = LocaLogger(group_name='redis')

try:
    r.ping()
    # Clear all items form the list to make sure that there are not existing events
    # from prior lola invocations that remain
    while r.lpop(LOLA_REDIS_LIST_NAME) is not None:
        pass
except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError, ConnectionError):
    logger.log_warning_msg("Could not connect to Redis. Redis is required for serving Lambdas.")
    exit()

class BaseServer(object):

    logger = LocaLogger(group_name='baseser')

    def execute_cli_cmd(self, 
        cmd: List[str], 
        build_dir: str = None,
        use_shell: bool = False
    ) -> None:
        """Executes an arbitrary function on the command line. Usage of this should only
        include `sam` commands.

        :param cmd: The command to submit
        :param build_dir: Whether or not to execute this command from the working
                               directory where the build exists.
        :return:
        """
        _run_cmd = ' '.join(cmd) if use_shell else cmd
        __log_cmd = ' '.join(_run_cmd) if isinstance(_run_cmd, list) else _run_cmd
        self.logger.log_info_msg(f'''Beginning to execute command: `{__log_cmd}`''')
        if build_dir:
            p = Popen(_run_cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, cwd=build_dir, shell=use_shell)
        else:
            p = Popen(_run_cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, shell=use_shell)
        while True:
            line_b = p.stdout.readline()
            if not line_b:
                break
            line = line_b.decode('utf-8').strip()
            self.logger.log_info_for_group(line)
        p.terminate()
        p.wait()

    @NotImplementedError
    def cleanup(self) -> None:
        """Function that should be overridden by each sub class to clean up any
        resources that were secured during the localambda execution. Not currently 
        used by any inhereted classes but may be in future.
        """
        pass


class LambdaServer(BaseServer):
    """The LambdaServer is responsible for locally serving the resources for a single
    repository and for capturing the port and hostname (generally localhost) for
    which the resource is served.

    The LambdaServer also serializes the routing information and writes it to Redis where
    the mitmproxy application picks it up and creates MatchedFlows.
    """
    _AWS_LAMBDA_URL = 'https://lambda.{}.amazonaws.com/2015-03-31/functions/'
    LOCALHOST = 'http://127.0.0.1:'
    LOCAL_HOST_ENDPOINT = '/2015-03-31/functions/'

    def __init__(self, deploy_name: str, stack_details: dict, exclude_ports: list = None):
        """Instantiates a LambdaServer class

        :param deploy_name: The logical name of deployed stack, primarily used for displaying log messages
        :param stack_details: A set of details that comes from the configurations
        :param exclude_ports: An optional list of ports to exclude when selecting a new port
        """
        self.deploy_name = deploy_name
        self.stack_details = stack_details
        self.stack_name = stack_details['stack_name']
        self.build_dir = stack_details['build_dir']
        self.serve_dir = stack_details['serve_dir']
        self.build_template = stack_details['build_template']
        self.serve_template = stack_details['serve_template']
        self.AWS_LAMBDA_URL = self._AWS_LAMBDA_URL.format(stack_details['region'])
        self.port = None
        self.exclude_ports = exclude_ports if exclude_ports else []
        self.get_available_port()
        self.logger = LocaLogger(group_name=self.deploy_name)

    def get_available_port(self) -> None:
        """Retrieves an available port on the machine that can be used to route traffic
        to the local AWS services deployed
        """
        while True:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                s.bind(('', 0))
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                port_val = s.getsockname()[1]
                if port_val not in self.exclude_ports:
                    self.port = port_val
                    break

    def serialize_for_mitm(self) -> None:
        """Serializes the configurations for the route to send to the man-in-the-middle
        by writing the serialized data to Redis.
        """
        routes = []
        for lambda_route in self.stack_details['proxy_routes']:
            route_set = {
                'from_route': f'{self.AWS_LAMBDA_URL}{self.stack_name}-{lambda_route["from"]}',
                'to_route': f'{self.LOCALHOST}{self.port}{self.LOCAL_HOST_ENDPOINT}{lambda_route["to"]}'
            }
            routes.append(route_set)

        r.lpush(LOLA_REDIS_LIST_NAME, json.dumps(routes))

    def get_build_script(self) -> List[str]:
        """Retrieves the command to execute to serve the resources in the repo provided.

        :return: A list of strings to start the services
        """
        return [
            'sam',
            'build',
            '--use-container',
            '--template',
            self.build_template,
            '--build-dir',
            self.build_dir
        ]

    def get_serve_script(self) -> List[str]:
        """Retrieves the command to execute to serve the resources in the repo provided.

        :return: A list of strings to start the services
        """
        return [
            'sam',
            'local',
            'start-lambda',
            '-p',
            f'{self.port}',
            '--template',
            self.serve_template,
            '--parameter-overrides',
            '"ParameterKey=Verify_SSL,ParameterValue=false"'
        ]

    @threadify
    def serve_and_wait(self) -> None:
        """Serves a lambda locally and waits for the user to provide a system exit (ctrl+c).

        :return: None
        """
        self.serialize_for_mitm()
        self.logger.log_info_msg(f'Beginning to serve {self.serve_template}')

        # Sleep for a short period of time so that all output logs are shown together
        time.sleep(.1)

        serve_script = self.get_serve_script()
        self.execute_cli_cmd(serve_script, build_dir=self.build_dir)

    def build_resources(self) -> None:
        """Executed within a new different thread. Executes the build commands for sam build"""
        build_script = self.get_build_script()
        self.execute_cli_cmd(build_script)
        self.copy_build_to_serve()

    def copy_build_to_serve(self):
        # Forcibly remove all build resources
        if os.path.exists(self.serve_dir):
            shutil.rmtree(self.serve_dir)

        copy_cmds = ['cp', '-r', f'{self.build_dir}', self.serve_dir]
        self.execute_cli_cmd(copy_cmds)
    
    def cleanup(self) -> None:
        self.logger.log_info_msg("Nothing to cleanup")
