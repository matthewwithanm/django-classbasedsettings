from django.conf import global_settings
import re


class DjangoDefaults(object):
    pass


class Debug:
    """A mixin for a debug settings class."""
    DEBUG = True


class Production:
    """A mixin for turning off debug mode."""
    DEBUG = False


for attr in vars(global_settings):
    if re.match(r'^[^_]', attr):
        setattr(DjangoDefaults, attr, getattr(global_settings, attr))
