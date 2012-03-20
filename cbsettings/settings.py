from django.conf import global_settings
import re


class DjangoDefaults(object):
    pass


for attr in vars(global_settings):
    if re.match(r'^[^_]', attr):
        setattr(DjangoDefaults, attr, getattr(global_settings, attr))
