import cbsettings


def unload_settings():
    import django.conf
    reload(django.conf)


def load_settings(settings):
    unload_settings()
    cbsettings.configure(settings)
    from django.conf import settings
    return settings
