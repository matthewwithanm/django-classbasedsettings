from django.conf import settings as djsettings
from django.utils.importlib import import_module
import re
import os
from .exceptions import InvalidSettingsFactory, SettingsFactoryDoesNotExist
from .switching import switcher


ENVIRONMENT_VARIABLE = 'DJANGO_SETTINGS_FACTORY'


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
                dir(settings_obj) if re.match(r'^[^_]', str(k)))
        djsettings.configure(**settings_dict)

        # We need to return the module so that it can be passed to execute_manager in manage.py. But should we use module of settings class or factory? THERE'S GOT TO BE A BETTER WAY!!
        return import_module(settings_obj.__class__.__module__), settings_obj
    else:
        raise InvalidSettingsFactory('%s is not a valid settings factory.'
            ' Please provide something of the form'
            ' `path.to.MySettingsFactory`' % factory)
