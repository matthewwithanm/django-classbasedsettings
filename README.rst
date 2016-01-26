This project allows you to define your Django project's settings using classes
instead of modules. Among other things, this allows you to use inheritance and
calculated properties.

.. image:: https://secure.travis-ci.org/matthewwithanm/django-classbasedsettings.png?branch=develop
   :target: http://travis-ci.org/matthewwithanm/django-classbasedsettings


Installation
============

The easiest way to install is by using pip:

.. code-block:: sh

    pip install django-classbasedsettings

However you can also just drop the "cbsettings" folder into your pythonpath.


Setup
=====

The places where you're currently setting ``DJANGO_SETTINGS_MODULE``, you'll have
to instead call ``cbsettings.configure``. So your manage.py will look something
like this:

.. code-block:: python

    #!/usr/bin/env python
    import os
    import sys
    import cbsettings

    if __name__ == "__main__":
        os.environ.setdefault('DJANGO_SETTINGS_FACTORY', 'path.to.MySettings')
        cbsettings.configure()

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

You'll have to make a similar modification to your wsgi file:

.. code-block:: python

    import os
    import cbsettings
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault('DJANGO_SETTINGS_FACTORY', 'path.to.MySettings')
    cbsettings.configure()

    application = get_wsgi_application()


Usage
=====


Basic
-----

The only real change you need to make to the settings.py file that Django
creates for you is to nest all the variables in a class:

.. code-block:: python

    from cbsettings import DjangoDefaults

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

        # etc, etc

Notice that the class extends ``DjangoDefaults``. By inheriting from this class,
you get all the default settings values that Django normally composites your
settings with. (These are pulled in from ``django.conf.global_settings`` so
they'll track with your version of Django, not classbasedsettings.) You can
also do stuff like this:

.. code-block:: python

    class MySettings(DjangoDefaults):

        STATICFILES_FINDERS = DjangoDefaults.STATICFILES_FINDERS + (
            'my.custom.StaticFileFinder',
        )

        # etc

These are just normal Python classes, so you can do anything you normally can:

.. code-block:: python

    class MySettings(DjangoDefaults):

        @property
        def TEMPLATE_DEBUG(self):
            # Now a subclass can override DEBUG and TEMPLATE_DEBUG will be changed accordingly
            return self.DEBUG

        # etc

Callable properties are automatically called:

.. code-block:: python

    class MySettings(DjangoDefaults):

        TEMPLATE_DEBUG = lambda s: s.DEBUG

...unless you don't want them to be:

.. code-block:: python

    from cbsettings import callable_setting

    class MySettings(DjangoDefaults):

        @callable_setting
        def SOME_SETTING(self, *args, **kwargs):
            # This setting is actually a callable. The decorator tells cbsettings
            # not to invoke it to get a settings value.
            .
            .
            .

        # You can also use the decorator with functions defined elsewhere
        SOME_OTHER_SETTING = callable_setting(my_function)

You can also prevent your callable settings from receiving a "self" argument:

.. code-block:: python

    from cbsettings import callable_setting

    class MySettings(DjangoDefaults):

        @callable_setting(takes_self=False)
        def SOME_SETTING(*args, **kwargs):
            .
            .
            .

        SOME_OTHER_SETTING = callable_setting(takes_self=False)(my_function)


Per-App Mixins
--------------

Two classes are provided to save you from having to type out long setting names:
``PrefixedSettings`` and ``Appsettings``. These are meant for declaring subsets
of your settings which share a prefix. The classes can then be mixed into your
real settings class.

``PrefixedSettings`` will apply an arbitrary prefix, which can be provided via
a Meta class. If none is specified, it will extract the prefix from the class
name:

.. code-block:: python

    from cbsettings import PrefixedSettings

    class MyFancySettings(PrefixedSettings):
        VALUE = 5

The above will result in a setting named ``MY_FANCY_VALUE``. (You would get the
same result by naming the class ``MyFancy``—without the "Settings" suffix.) If a
prefix is specified, it will be used without manipulation. In other word:

.. code-block:: python

    class MyFancySettings(PrefixedSettings):
        VALUE = 5

        class Meta:
            prefix = 'hello'

will result in a setting named ``helloVALUE``.

``AppSettings`` is similar, but it uses a different Meta attribute and does a
little extra formatting. In most cases, you'll want to use ``AppSettings`` and
not ``PrefixedSettings``:

.. code-block:: python

    from cbsettings import AppSettings

    class MyAppSettings(AppSettings):
        VALUE = 5

will result in a setting named ``MY_APP_VALUE``. (You would get the same result
by naming the class ``MyApp``—without the "Settings" suffix.) If an app name is
provided explicitly, it will be uppercased and an underscore will be appended:

.. code-block:: python

    class MyAppSettings(AppSettings):
        VALUE = 5

        class Meta:
            app_name = 'somebody_elses_app'

will result in a setting named ``SOMEBODY_ELSES_APP_VALUE``.


Using a Settings Factory
------------------------

You might be thinking that hardcoding your settings class into files is just as
bad as Django's hardcoding of the settings module. That's true. Which is why
``configure()`` can be passed the path to any callable that returns a settings
object instance. So your manage.py might instead look like this:

.. code-block:: python

    #!/usr/bin/env python
    import sys
    import cbsettings

    if __name__ == "__main__":
        cbsettings.configure('path.to.my.settings.factory')

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

Then, in ``path/to/my/settings.py``:

.. code-block:: python

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
handle these common cases, and allow you to easily define simple conditions of
your own. It also uses a more declarative syntax, which makes it more organized
than a factory method. Here's how you use it in your settings file:

.. code-block:: python

    from cbsettings import DjangoDefaults, switcher

    class MyProductionSettings(DjangoDefaults):
        DEBUG = False
        # etc

    class MyDevSettings(DjangoDefaults):
        DEBUG = True
        # etc

    class MyTestingSettings(MyProductionSettings):
        SOME_VAR = 'whatever'

    # You can use one of the preregistered conditions by passing kwargs. The
    # first class whose conditions are all met will be used.
    switcher.register(MyTestSettings, testing=True)
    switcher.register(MyDevSettings, hostnames=['mycompuer.home', 'billscomputer.home'])
    switcher.register(MyProductionSettings, hostnames=['theserver.com'])

    # ...or you can define your own simple checks as positional arguments. If
    # all of the values are truthy (and any kwarg checks pass), the class will
    # be used.
    switcher.register(MyDevSettings, 'dev.mysite.com' in __file__)
    switcher.register(MyDevSettings, os.environ.get('DEV'))

    # Callable positional arguments will be called, then checked for truthiness.
    switcher.register(MyDevSettings, lambda: randint(1, 2) == 2)

You can also use ``switcher.register`` as a class decorator:

.. code-block:: python

    @switcher.register(hostnames=['theserver.com'])
    class MyProductionSettings(DjangoDefaults):
        DEBUG = False
        # etc

Then, wherever you're calling ``configure``, pass it your module's ``switcher``
variable:

.. code-block:: python

    cbsettings.configure('path.to.my.settings.switcher')
