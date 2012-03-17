from cbsettings import Conf
import inspect
import os
import re


try:
    CBSETTINGS_MODULE = os.environ['CBSETTINGS_MODULE']
except KeyError:
    from cbsettings.exceptions import CbSettingsModuleNotDefined
    raise CbSettingsModuleNotDefined('You must set CBSETTINGS_MODULE')

settings_module = __import__(CBSETTINGS_MODULE, fromlist=[''])


def default_factory():
    print os.environ
    # TODO: Better way to do this than checking type?
    config_classes = [cls for name, cls in vars(settings_module).items() if
        inspect.isclass(cls) and issubclass(cls, Conf) and cls is not Conf]

    active_confs = []
    for cls in config_classes:
        meta = getattr(cls, '_cbsettings_meta', None)
        is_active_attr = getattr(meta, 'is_active', None)
        is_active = is_active_attr() if callable(is_active_attr) else bool(is_active_attr)
        if is_active:
            active_confs.append(cls)

    if len(active_confs) > 1:
        raise Exception('You have more than one active class-based settings'
                ' conf (%s). That\'s not allowed.' % ', '.join(map(lambda x: x.__name__, active_confs)))
    return active_confs[0]() if active_confs else None


factory = getattr(settings_module, 'CBSETTINGS_FACTORY', default_factory)
conf = factory()

setting_items = dict((k, getattr(settings_module, k)) for k in dir(settings_module)).items()
if conf:
    setting_items += dict((k, getattr(conf, k)) for k in dir(conf)).items()

localvars = locals()
for attr, value in setting_items:
    if re.match(r'^[A-Z0-9_]+$', attr):
        localvars[attr] = value
