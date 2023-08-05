import psutil
import os

from .utility import Utility
from wafec_tests_openstack_base.interception import generate_key
from wafec_tests_openstack_base.clients import InterceptionAgentClient
from ._configuration import interception_config

__all__ = [
    'Interception'
]


class Interception(object):
    @staticmethod
    def add_proxy_interception_info(name, x=None, trace=None):
        p = psutil.Process()
        ps = p.name()
        kwargs = {
            'ps': ps,
            'name': name,
            'x': Utility.fullname(x),
            'trace': trace,
            'asynchronous': True
        }
        client = InterceptionAgentClient(interception_config.url)
        client.post(**kwargs)

    @staticmethod
    def should_handle_fault(name, x, trace):
        if os.path.exists(interception_config.dat_file):
            p = psutil.Process()
            ps = p.name()
            key = generate_key(name, x, trace, ps)
            with open(interception_config.dat_file, 'r') as dat_file:
                lines = dat_file.read().splitlines()
            if lines:
                line_parts = lines[0].split(' ')
                if line_parts and len(line_parts) > 1:
                    dat_key = line_parts[0]
                    if dat_key == key:
                        return line_parts[1]
        return False



