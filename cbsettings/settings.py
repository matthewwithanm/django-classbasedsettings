from django.conf import global_settings
from .decorators import callable_setting


class DjangoDefaults(object):
    pass


for attr in vars(global_settings):
    if not attr.startswith('_'):
        value = getattr(global_settings, attr)
        if callable(value):
            value = callable_setting(value)
        setattr(DjangoDefaults, attr, value)
