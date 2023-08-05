import psutil
import unittest

from wafec_tests_openstack_stub._configuration import interception_config
from wafec_tests_openstack_base.interception import generate_key
from wafec_tests_openstack_stub.interception import Interception

interception_config.dat_file = "../../resources/dat_file.txt"


class InterceptionTests(unittest.TestCase):
    def setUp(self):
        self.x = 'test'
        self.trace = 'test'
        self.name = 'test'
        self.ps = psutil.Process().name()
        self.key = generate_key(self.name, self.x, self.trace, self.ps)
        self.method = 'fault_test'
        with open(interception_config.dat_file, 'w') as dat_file:
            dat_file.write(f'{self.key} {self.method}\n')

    def test_should_handle_fault(self):
        result = Interception.should_handle_fault(self.name, self.x, self.trace)
        self.assertEqual(self.method, result)

