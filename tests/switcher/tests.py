from cbsettings.exceptions import NoMatchingSettings
import socket
import unittest
from ..utils import load_settings


gethostname = socket.gethostname


def patched_gethostname(*args, **kwargs):
    return 'testhost'


class SwitcherTestCase(unittest.TestCase):

    def setUp(self):
        socket.gethostname = patched_gethostname

    def tearDown(self):
        socket.gethostname = gethostname

    def test_hostname_switch(self):
        """
        Test that the hostname switch works correctly.

        """
        settings = load_settings('tests.test_settings.switcher_a')
        self.assertTrue(getattr(settings, 'IS_A', False))

    def test_hostname_nomatch(self):
        """
        Test that the hostname switch errors when there is no match.

        """
        self.assertRaises(NoMatchingSettings, load_settings,
                'tests.test_settings.switcher_b')

    def test_simple_checks(self):
        settings = load_settings('tests.test_settings.switcher_c')
        self.assertTrue(getattr(settings, 'IS_A', False))

    def test_simple_callable_checks(self):
        settings = load_settings('tests.test_settings.switcher_d')
        self.assertTrue(getattr(settings, 'IS_A', False))
