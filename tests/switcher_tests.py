from cbsettings.exceptions import NoMatchingSettings
from nose import with_setup
from nose.tools import assert_true, assert_raises
import socket
from .utils import load_settings


gethostname = socket.gethostname


def patched_gethostname(*args, **kwargs):
    return 'testhost'


def patch_hostname():
    socket.gethostname = patched_gethostname


def unpatch_hostname():
    socket.gethostname = gethostname


@with_setup(patch_hostname, unpatch_hostname)
def test_hostname_switch():
    """
    Test that the hostname switch works correctly.

    """
    settings = load_settings('tests.settings.switcher_a')
    assert_true(getattr(settings, 'IS_A', False))


@with_setup(patch_hostname, unpatch_hostname)
def test_hostname_nomatch():
    """
    Test that the hostname switch errors when there is no match.

    """
    assert_raises(NoMatchingSettings, load_settings,
                  'tests.settings.switcher_b')


@with_setup(patch_hostname, unpatch_hostname)
def test_simple_checks():
    settings = load_settings('tests.settings.switcher_c')
    assert_true(getattr(settings, 'IS_A', False))


@with_setup(patch_hostname, unpatch_hostname)
def test_simple_callable_checks():
    settings = load_settings('tests.settings.switcher_d')
    assert_true(getattr(settings, 'IS_A', False))
