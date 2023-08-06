import sys
from os import path, system
from subprocess import Popen, PIPE, STDOUT
import sysconfig
from typing import List

from .localogger import LocaLogger
from .decorators import threadify


class LocalHttpsProxy(object):
    """Manages a local HTTPS proxy server that routes all traffic to a specific
    host through the local proxy
    """
    # TODO: currently only enabled for MAC and Ubuntu, this class should be OS agnostic
    REROUTE_SCRIPT = path.join(path.dirname(path.dirname(path.realpath(__file__))), 
                               'mitm_scripts',
                               'reroute_traffic.py')

    def __init__(self, proxy_port: int = 8766, aws_region: str = 'us-west-2', network_service: str = 'Wi-Fi'):
        self.proxy_port = proxy_port
        self.proxy_set = False
        self.aws_region = aws_region
        self.network_service = network_service  # TODO: This class should lookup if Wi-Fi or Ethernet is used
        self.logger = LocaLogger('Local HTTPs Proxy')

    @staticmethod
    def is_proxy_loggable_message(msg: str) -> bool:
        is_loggable = True
        if ': clientconnect' in msg:
            is_loggable = False
        if ': clientdisconnect' in msg:
            is_loggable = False
        return is_loggable

    def run_cmd(self, cmd: List[List[str]]) -> None:
        for command in cmd:
            p = Popen(command, stdout=PIPE, stderr=STDOUT, bufsize=1)
            with p.stdout:
                for line_b in iter(p.stdout.readline, b''):
                    line = line_b.decode('utf-8').strip()
                    if self.is_proxy_loggable_message(line):
                        self.logger.log_info_for_group(line)
            p.terminate()
            p.wait()

    @property
    def run_proxy_server_cmd(self) -> List[List[str]]:
        return [
            [
                'mitmdump',
                '-p',
                str(self.proxy_port),
                '--allow-hosts',
                'amazonaws.com',
                '-s',
                self.REROUTE_SCRIPT
            ]
        ]
    
    @property
    def python_path(self) -> str:
        """Returns the python path for the current python executable"""
        python_path = sysconfig.get_paths()["purelib"]
        return f"PYTHONPATH={python_path}"

    @NotImplementedError
    def configure_proxy_cmd(self):
        return

    @NotImplementedError
    def turn_on_proxy_cmd(self):
        return

    @NotImplementedError
    def turn_off_proxy_cmd(self):
        return

    def turn_on_proxy(self) -> None:
        self.logger.log_info_msg(
            f'''Setting proxy configuration with command: "{' && '.join([' '.join(cmd) for cmd in 
            self.configure_proxy_cmd])}"'''
        )
        self.run_cmd(self.configure_proxy_cmd)

        self.logger.log_info_msg(
            f'''Turning proxy configuration on with command: "{' '.join(self.turn_on_proxy_cmd[0])}"'''
        )
        self.run_cmd(self.turn_on_proxy_cmd)
        self.proxy_set = True

    def turn_off_proxy(self) -> None:
        self.logger.log_info_msg(
            f'''Turning proxy configuration off with command: "{' '.join(self.turn_off_proxy_cmd[0])}"'''
        )
        self.run_cmd(self.turn_off_proxy_cmd)
        self.proxy_set = False

    @threadify
    def run_proxy_server(self, **kwargs) -> None:
        self.turn_on_proxy()
        cmd = self.run_proxy_server_cmd
        self.logger.log_info_msg(f'''Turning HTTPS proxy server on with command: "{' '.join(cmd[0])}"''')
        self.run_cmd(cmd)


class LinuxLocalHttpsProxy(LocalHttpsProxy):

    @property
    def configure_proxy_cmd(self) -> List[List[str]]:
        return [
            [
                'gsettings',
                'set',
                'org.gnome.system.proxy.https',
                'host',
                'localhost'
            ],
            [
                'gsettings',
                'set',
                'org.gnome.system.proxy.https',
                'port',
                str(self.proxy_port)
            ]
        ]

    @property
    def turn_on_proxy_cmd(self) -> List[List[str]]:
        return [
            [
                'gsettings',
                'set',
                'org.gnome.system.proxy',
                'mode',
                "'manual'"
            ]
        ]

    @property
    def turn_off_proxy_cmd(self) -> List[List[str]]:
        return [
            [
                'gsettings',
                'set',
                'org.gnome.system.proxy',
                'mode',
                "'none'"
            ]
        ]


class MacLocalHttpsProxy(LocalHttpsProxy):

    @property
    def configure_proxy_cmd(self) -> List[List[str]]:
        return [
            [
                'networksetup',
                '-setsecurewebproxy',
                self.network_service,
                'localhost',
                str(self.proxy_port)
            ]
        ]

    @property
    def turn_on_proxy_cmd(self) -> List[List[str]]:
        return [
            [
                'networksetup',
                '-setsecurewebproxystate',
                self.network_service,
                'on'
            ]
        ]

    @property
    def turn_off_proxy_cmd(self) -> List[List[str]]:
        return [
            [
                'networksetup',
                '-setsecurewebproxystate',
                self.network_service,
                'off'
            ]
        ]
