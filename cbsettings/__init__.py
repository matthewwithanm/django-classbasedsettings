import django
from django.utils.importlib import import_module
import imp
import os
import sys
from .exceptions import InvalidSettingsFactory, SettingsFactoryDoesNotExist
from .settings import DjangoDefaults
from .switching import switcher
from .version import *


ENVIRONMENT_VARIABLE = 'DJANGO_SETTINGS_FACTORY'
DJANGO_SETTINGS_MODULE = django.conf.ENVIRONMENT_VARIABLE


def configure(factory=None, **kwargs):
    if not factory:
        factory = os.environ.get(ENVIRONMENT_VARIABLE)
        if not factory:
            raise ImportError('Settings could not be imported because'
                    ' configure was called without arguments and the environment'
                    ' variable %s is undefined.' % ENVIRONMENT_VARIABLE)
    if '.' in factory:
        factory_module, factory_name = factory.rsplit('.', 1)
        try:
            mod = import_module(factory_module)
            factory_obj = getattr(mod, factory_name)
        except (ImportError, AttributeError), err:
            raise SettingsFactoryDoesNotExist('The object "%s" could not be'
                    ' found (Is it on sys.path?): %s' % (factory, err))

        settings_obj = factory_obj()
        settings_dict = dict((k, getattr(settings_obj, k)) for k in
                dir(settings_obj) if not str(k).startswith('_'))

        if 'SETTINGS_MODULE' not in settings_dict:
            settings_dict['SETTINGS_MODULE'] = '%s_%s_unrolledcbsettings' % (
                    factory_module, factory_name)

        # Create the settings module.
        parts = settings_dict['SETTINGS_MODULE'].split('.')
        parent_module = None
        for i in range(len(parts)):
            module_fullname = '.'.join(parts[:i + 1])
            module_name = parts[i]
            try:
                module = __import__(module_fullname, fromlist=[''])
            except ImportError:
                module = imp.new_module(module_fullname)
                sys.modules[module_fullname] = module

            if parent_module:
                setattr(parent_module, module_name, module)
            parent_module = module

        # Unroll the settings into a new module.
        for k, v in settings_dict.items():
            setattr(module, k, v)

        os.environ[DJANGO_SETTINGS_MODULE] = settings_dict['SETTINGS_MODULE']

        return mod, settings_obj
    else:
        raise InvalidSettingsFactory('%s is not a valid settings factory.'
            ' Please provide something of the form'
            ' `path.to.MySettingsFactory`' % factory)
