This project allows you to define your Django project's settings using classes
instead of modules. Among other things, this allows you to use inheritance and
calculated properties.


Installation
============

The easiest way to install is by using pip::

    pip install -e git://github.com/matthewwithanm/django-classbasedsettings.git#egg=django-classbasedsettings

However you can also just drop the "cbsettings" folder into your pythonpath.


Setup
=====

The places where you're currently setting ``DJANGO_SETTINGS_MODULE``, you'll have
to instead call ``cbsettings.configure``. So your manage.py will look something
like this::

    #!/usr/bin/env python
    from django.core.management import execute_manager
    import cbsettings

    settings_module, settings_obj = cbsettings.configure('path.to.MySettings')

    if __name__ == "__main__":
        execute_manager(settings_module)

You'll have to make a similar modification to your wsgi file.


Usage
=====


Basic
-----

The only real change you need to make to the settings.py file that Django
creates for you is to nest all the variables in a class::

    from cbsettings.settings import DjangoDefaults

    class MySettings(DjangoDefaults):

        ADMINS = (
            # ('Your Name', 'your_email@example.com'),
        )

        MANAGERS = ADMINS

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.',
                'NAME': '',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }

Notice that the class extends ``DjangoDefaults``. By inheriting from this class,
you get all the default settings values that Django normally composites your
settings with. (These are pulled in from ``django.conf.global_settings`` so
they'll track with your version of Django, not classbasedsettings.) You can
also do stuff like this::

    class MySettings(DjangoDefaults):

        STATICFILES_FINDERS = DjangoDefaults.STATICFILES_FINDERS + (
            'my.custom.StaticFileFinder',
        )

These are just normal Python classes, so you can do anything you normally can::

    class MySettings(DjangoDefaults):

        @property
        def TEMPLATE_DEBUG(self):
            # Now a subclass can override DEBUG and TEMPLATE_DEBUG will be changed accordingly
            return self.DEBUG


Using a Settings Factory
------------------------

You might be thinking that hardcoding your settings class into files is just as
bad as Django's hardcoding of the settings module. That's true. Which is why
``configure()`` can be passed the path to any callable that returns a settings
object instance. So your manage.py might instead look like this::

    #!/usr/bin/env python
    from django.core.management import execute_manager
    import cbsettings

    settings_module, settings_obj = cbsettings.configure('path.to.my.settings.factory')

    if __name__ == "__main__":
        execute_manager(settings_module)

Then, in ``path/to/my/settings.py``::

    def factory():
        if 'DEV' in os.environ:
            return MyDebugSettings()
        else:
            return MyProductionSettings()

Now you can easily change which settings class you're using based on whatever
conditions you want without having to make modifications to multiple files.


Using Switcher
--------------

Using a factory method to determine which settings class to use is a powerful
feature! But usually you'll want to switch settings classes based on the same
kinds of conditions, so django-classbasedsettings comes with a factory that'll
handle these common cases. It also uses a more declarative syntax, which makes
it more organized than a factory method. Here's how you use it in your settings
file::

    from cbsettings import switcher
    from cbsettings.settings import DjangoDefaults

    class MyProductionSettings(DjangoDefaults):
        DEBUG = False
        # etc

    class MyDevSettings(DjangoDefaults):
        DEBUG = True
        # etc

    switcher.register(MyProductionSettings, hostnames=['theserver.com'])
    switcher.register(MyDevSettings, hostnames=['mycompuer.home', 'billscomputer.home'])

You can also use ``switcher.register`` as a decorator::

    from cbsettings import switcher
    from cbsettings.settings import DjangoDefaults

    @switcher.register(hostnames=['theserver.com'])
    class MyProductionSettings(DjangoDefaults):
        DEBUG = False
        # etc

    @switcher.register(hostnames=['mycompuer.home', 'billscomputer.home'])
    class MyDevSettings(DjangoDefaults):
        DEBUG = True
        # etc

Then, wherever you're calling ``configure``, pass it your module's ``switcher``
variable::

    cbsettings.configure('path.to.my.settings.switcher')
