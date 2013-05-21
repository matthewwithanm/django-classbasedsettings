import imp
import sys


def new_module(name):
    """
    Do all of the gruntwork associated with creating a new module.

    """
    parent = None
    if '.' in name:
        parent_name = name.rsplit('.', 1)[0]
        parent = __import__(parent_name, fromlist=[''])

    module = imp.new_module(name)
    sys.modules[name] = module
    if parent:
        setattr(parent, name.rsplit('.', 1)[1], module)
    return module


class SettingsImporter(object):
    def __init__(self, module_name, settings):
        self.module_name = module_name
        self.settings = settings

    def find_module(self, name, path=None):
        if name == self.module_name:
            return self

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        # Unroll the settings into a new module.
        module = new_module(self.module_name)
        for k, v in self.settings.items():
            if callable(v) and not getattr(v, 'is_callable_setting', False):
                v = v()
            setattr(module, k, v)

        return module
