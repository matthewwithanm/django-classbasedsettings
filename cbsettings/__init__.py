from builtins import str
import os
import sys

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

import django

from .exceptions import InvalidSettingsFactory, SettingsFactoryDoesNotExist
from .decorators import callable_setting  # noqa
from .importers import SettingsImporter
from .settings import DjangoDefaults, AppSettings, PrefixedSettings  # noqa
from .switching import switcher  # noqa
from cbsettings.pkgmeta import *  # noqa


ENVIRONMENT_VARIABLE = 'DJANGO_SETTINGS_FACTORY'
DJANGO_SETTINGS_MODULE = django.conf.ENVIRONMENT_VARIABLE


def configure(factory=None, **kwargs):
    if not factory:
        factory = os.environ.get(ENVIRONMENT_VARIABLE)
        if not factory:
            raise ImportError(
                'Settings could not be imported because configure was called'
                ' without arguments and the environment variable %s is'
                ' undefined.' % ENVIRONMENT_VARIABLE)
    if '.' in factory:
        factory_module, factory_name = factory.rsplit('.', 1)
        try:
            mod = import_module(factory_module)
            factory_obj = getattr(mod, factory_name)
        except (ImportError, AttributeError) as err:
            raise SettingsFactoryDoesNotExist(
                'The object "%s" could not be found (Is it on sys.path?):'
                ' %s' % (factory, err))

        settings_obj = factory_obj()
        settings_dict = dict((k, getattr(settings_obj, k)) for k in
                             dir(settings_obj) if not str(k).startswith('_'))

        if 'SETTINGS_MODULE' not in settings_dict:
            settings_dict['SETTINGS_MODULE'] = (
                '%s_%s_unrolledcbsettings' % (factory_module, factory_name))

        # Create an importer for handling imports of our constructed settings
        # module.
        sys.meta_path.insert(
            0,
            SettingsImporter(settings_dict['SETTINGS_MODULE'], settings_dict)
        )

        os.environ[DJANGO_SETTINGS_MODULE] = settings_dict['SETTINGS_MODULE']

        return mod, settings_obj
    else:
        raise InvalidSettingsFactory(
            '%s is not a valid settings factory. Please provide something of'
            ' the form `path.to.MySettingsFactory`' % factory)
