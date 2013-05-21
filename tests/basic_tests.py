from nose.tools import assert_true, assert_false
from .utils import load_settings


def test_load():
    """
    Test that class based settings can be loading (and also verify that our method of unloading settings is working!)

    """
    settings = load_settings('tests.settings.A')
    assert_true(getattr(settings, 'IS_A', False))

    settings = load_settings('tests.settings.B')
    assert_false(getattr(settings, 'IS_A', False))
    assert_true(getattr(settings, 'IS_B', False))


def test_inheritance():
    settings = load_settings('tests.settings.Child')
    assert_true(getattr(settings, 'PARENT_ATTR', False))
    assert_true(getattr(settings, 'CHILD_ATTR', False))


def test_django_defaults():
    settings = load_settings('tests.settings.A')
    assert_true(hasattr(settings, 'INSTALLED_APPS'))


def test_attr_access():
    settings = load_settings('tests.settings.A')
    parent_name, module_name = settings.SETTINGS_MODULE.rsplit('.', 1)
    parent = __import__(parent_name, fromlist=[''])
    getattr(parent, module_name)


def test_reload():
    settings = load_settings('tests.settings.A')
    module = __import__(settings.SETTINGS_MODULE, fromlist=[''])
    reload(module)
