import os
import sys
import time

from .serve import LambdaServer
from .proxy import MacLocalHttpsProxy, LinuxLocalHttpsProxy
from . import configuration, localogger


def get_proxy():
    if sys.platform == 'linux':
        return LinuxLocalHttpsProxy
    return MacLocalHttpsProxy


class CommandRunner(object):
    """Orchestrates all of the commands to run and the sequence in which they should be run.
    Delegates with the following logic:
        - repo / stack specific actions are given to LambdaServers
    """
    STEP_ORDER = ['build', 'serve']
    STAY_OPEN_CMDS = ['serve']

    def __init__(self, config=None):
        self.logger = localogger.LocaLogger(group_name='LOLA Command Runner', group_id=0)
        self.configs = configuration.ConfigManager(config)
        self.steps = []
        self.command_runners = []
        self.local_proxy = get_proxy()(aws_region=self.configs.lola_file_yaml['region'])

    def add_step(self, step, add_step) -> None:
        if add_step:
            if step == 'run':
                if 'build' not in self.steps:
                    self.steps.append('build')
                if 'serve' not in self.steps:
                    self.steps.append('serve')
            elif step == 'setup' and len(self.steps) != 0:
                self.logger.log_error_msg('Setup cannot be called with other steps')
                sys.exit()
            self.steps.append(step)

    def generate_command_runners_from_configs(self) -> None:
        """Creates a LambdaServer object for each stack in the configs. LambdaServers need to reserve a
        port to run, reserved ports are made available to each LambdaServer to prevent accidently
        selecting the same port.
        """
        self.logger.log_info_msg('Getting configs')
        reserved_ports = []
        
        if 'stacks' in self.configs.lola_file_yaml:
            for stack in self.configs.lola_file_yaml['stacks']:
                stack_details = list(stack.items())[0]
                logical_name, stack_deployment = stack_details[0], stack_details[1]
                b = LambdaServer(deploy_name=logical_name, stack_details=stack_deployment, exclude_ports=reserved_ports)
                reserved_ports.append(b.port)
                self.command_runners.append(b)

    def _run(self) -> None:
        """Executes the main flow for the Command Runner. Tasks are executed sequentially to each other
            but are parallelized within each task.

            For example, if 3 stacks are being deployed locally and the build and serve commands are provided,
            the three repos will be built in parallel, however, they will only be served after all of the builds
            are completed.
        """
        self.generate_command_runners_from_configs()
        for step in self.STEP_ORDER:
            if step in self.steps:
                if step == 'serve':
                    self.local_proxy.run_proxy_server()
                func = getattr(self, step)
                self.logger.log_info_msg(f'Beginning to run step: {step}')
                func()

    def run(self) -> None:
        """Wraps the _run process to allow for the user to provide keyboard / system exit
        commands. Once one of these exceptions occurs, CommandRunner attempts to shutdown
        and validate that all HTTPS proxy server configurations have been removed.
        """
        try:
            self._run()
            if any([cmd in self.steps for cmd in self.STAY_OPEN_CMDS]):
                while True:
                    time.sleep(100)
        except (KeyboardInterrupt, SystemExit):
            self.logger.log_warning_msg('Exit system event received, cleaning up resources')
            if self.local_proxy.proxy_set:
                self.local_proxy.turn_off_proxy()
                self.logger.log_info_msg('Proxy successfully removed')
            for cr in self.command_runners:
                cr.cleanup()
        finally:
            self.logger.log_info_msg('Have a good day!')

    def build(self):
        for server in [b for b in self.command_runners if isinstance(b, LambdaServer)]:
            server.build_resources()

    def serve(self) -> None:
        self.logger.log_info_msg('Beginning to serve deployments locally')
        for server in [b for b in self.command_runners if isinstance(b, LambdaServer)]:
            server.serve_and_wait()


def setup():
    user_home = os.path.expanduser('~')
    lola_home = os.path.join(user_home, 'lola')

    input("Time to get setup with \033[94m LocaLambda!\033[0m! This will only take a moment.. "
          "Press [enter] to continue   ")

    lola_loc = input(f"Enter the location to save your lola home directory. I will use this directory for configs, "
                     f"resources and temporary files (press enter to use {lola_home}): ")

    lola_rc = os.path.join(user_home, '.lolarc')
    lola_home = lola_loc or lola_home
    lola_save_loc = os.path.join(lola_home, 'lola.yaml')
    if not os.path.exists(os.path.dirname(lola_save_loc)):
        os.makedirs(os.path.dirname(lola_save_loc))

    with open(lola_rc, 'w') as f:
        f.write(f'lola_home: {lola_home}\nlola_file: {lola_save_loc}\n')

    print(f"Thanks! You're all set up! Don't forget you can always change the location of your" +
          f"\033[94m LocaLambda!\033[0m by adjusting the location here: {lola_rc}")
