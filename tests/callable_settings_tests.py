from nose.tools import assert_true
from .utils import load_settings


def test_autocall():
    settings = load_settings('tests.settings.CallableSettings')
    assert_true(settings.F1)


def test_donotcall():
    settings = load_settings('tests.settings.CallableSettings')
    value = settings.F2()
    assert_true(value)


def test_donotcall_noself():
    settings = load_settings('tests.settings.CallableSettings')
    value = settings.F3()
    assert_true(value)
