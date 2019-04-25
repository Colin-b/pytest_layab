import unittest

from pycommon_test import samba_mock
from smb.SMBConnection import SMBConnection


class SambaMockTest(unittest.TestCase):

    def test_context_manager_enter_exit(self):
        with SMBConnection("testuser", "testpwd", "testclient", "testmachine"):
            self.assertTrue(True)
