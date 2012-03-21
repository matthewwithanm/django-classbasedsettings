from django.conf import global_settings


class DjangoDefaults(object):
    pass


for attr in vars(global_settings):
    if not attr.startswith('_'):
        setattr(DjangoDefaults, attr, getattr(global_settings, attr))
