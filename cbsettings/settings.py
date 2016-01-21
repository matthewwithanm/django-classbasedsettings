from django.conf import global_settings
import re
from .decorators import callable_setting
from future.utils import with_metaclass


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
        try:
            PrefixedSettings
        except NameError:
            # Creating the PrefixedSettings class. Continue.
            pass
        else:
            if PrefixedSettings in bases:
                prefix = get_prefix(attrs, name)
                attrs = prefix_attributes(prefix, attrs)
        return super(PrefixedSettingsBase, cls).__new__(cls, name, bases,
                                                        attrs)


class AppSettingsBase(type):
    def __new__(cls, name, bases, attrs):
        try:
            AppSettings
        except NameError:
            # Creating the AppSettings class. Continue.
            pass
        else:
            if AppSettings in bases:
                prefix = get_prefix(attrs, name, use_app_name=True)
                attrs = prefix_attributes(prefix, attrs)
        return super(AppSettingsBase, cls).__new__(cls, name, bases, attrs)


class PrefixedSettings(with_metaclass(PrefixedSettingsBase, object)):
    pass


class AppSettings(with_metaclass(AppSettingsBase, object)):
    pass
