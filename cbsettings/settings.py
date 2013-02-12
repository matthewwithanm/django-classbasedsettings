from django.conf import global_settings
import re
from .decorators import callable_setting


prefix_pattern = re.compile(r'(?P<prefix>.*?)(Settings)?$')
caps_pattern = re.compile(r'([A-Z])')


class DjangoDefaults(object):
    pass


for attr in vars(global_settings):
    if not attr.startswith('_'):
        value = getattr(global_settings, attr)
        if callable(value):
            value = callable_setting(value)
        setattr(DjangoDefaults, attr, value)


def prefix_attributes(prefix, attrs):
    return dict(('%s%s' % (prefix, k), v) for k, v in attrs.items()
                if not k.startswith('_') and k != 'Meta')


def to_underscores(text):
    return caps_pattern.sub(r'_\1', text).strip('_')


def get_prefix(attrs, class_name, use_app_name=False):
    prefix = getattr(attrs.get('Meta', None), 'prefix', None)
    if prefix is None:
        if use_app_name:
            app_name = getattr(attrs.get('Meta', None), 'app_name', None)
            if app_name:
                prefix = '%s_' % to_underscores(app_name).upper()
    if prefix is None:
        prefix = prefix_pattern.match(class_name).groupdict()['prefix']
        prefix = '%s_' % to_underscores(prefix).upper()
    return prefix


class PrefixedSettingsBase(type):
    def __new__(cls, name, bases, attrs):
        prefix = get_prefix(attrs, name)
        new_attrs = prefix_attributes(prefix, attrs)
        return super(PrefixedSettingsBase, cls).__new__(cls, name, bases,
                                                        new_attrs)


class AppSettingsBase(type):
    def __new__(cls, name, bases, attrs):
        prefix = get_prefix(attrs, name, use_app_name=True)
        new_attrs = prefix_attributes(prefix, attrs)
        return super(AppSettingsBase, cls).__new__(cls, name, bases,
                                                   new_attrs)


class PrefixedSettings(object):
    __metaclass__ = PrefixedSettingsBase


class AppSettings(object):
    __metaclass__ = AppSettingsBase
