import unittest
from ..utils import load_settings


class BasicTestCase(unittest.TestCase):

    def test_load(self):
        """
        Test that class based settings can be loading (and also verify that our method of unloading settings is working!)

        """
        settings = load_settings('tests.test_settings.A')
        self.assertTrue(getattr(settings, 'IS_A', False))

        settings = load_settings('tests.test_settings.B')
        self.assertFalse(getattr(settings, 'IS_A', False))
        self.assertTrue(getattr(settings, 'IS_B', False))

    def test_inheritance(self):
        settings = load_settings('tests.test_settings.Child')
        self.assertTrue(getattr(settings, 'PARENT_ATTR', False))
        self.assertTrue(getattr(settings, 'CHILD_ATTR', False))

    def test_django_defaults(self):
        settings = load_settings('tests.test_settings.A')
        self.assertTrue(hasattr(settings, 'INSTALLED_APPS'))

    def test_attr_access(self):
        settings = load_settings('tests.test_settings.A')
        parent_name, module_name = settings.SETTINGS_MODULE.rsplit('.', 1)
        parent = __import__(parent_name, fromlist=[''])
        getattr(parent, module_name)
