from cbsettings import AppSettings, PrefixedSettings
from nose.tools import assert_true


class Some(PrefixedSettings):
    VALUE = True


class SomeSettings(PrefixedSettings):
    VALUE = True


class OtherSettings(PrefixedSettings):
    VALUE = True

    class Meta(object):
        prefix = 'special_'


class MyApp(AppSettings):
    VALUE = True


class MyAppSettings(AppSettings):
    VALUE = True


class OtherApp(AppSettings):
    VALUE = True

    class Meta(object):
        app_name = 'special'


class PrefixedSettingsSubclass(SomeSettings):
    UNPREFIXED = True


def test_prefixedsettings_classname():
    obj = Some()
    assert_true('SOME_VALUE' in dir(obj))


def test_prefixedsettings_suffixed_classname():
    obj = SomeSettings()
    assert_true('SOME_VALUE' in dir(obj))


def test_prefixedsettings_explicit_name():
    obj = OtherSettings()
    assert_true('special_VALUE' in dir(obj))


def test_appsettings_classname():
    obj = MyApp()
    assert_true('MY_APP_VALUE' in dir(obj))


def test_appsettings_suffixed_classname():
    obj = MyAppSettings()
    assert_true('MY_APP_VALUE' in dir(obj))


def test_appsettings_explicit_name():
    obj = OtherApp()
    assert_true('SPECIAL_VALUE' in dir(obj))


def test_mixin():
    obj = PrefixedSettingsSubclass()
    assert_true('UNPREFIXED' in dir(obj))
