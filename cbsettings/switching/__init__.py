import re
from ..exceptions import InvalidCondition, NoMatchingSettings
from . import checks


class NoSwitcher:
    """Used as a sentinel argument for Switcher.register"""
    pass


class BaseSwitcher(object):
    checks = {}

    def __init__(self):
        self._registry = []

    def add_check(self, name, check):
        """Adds a checking function to the switcher."""
        self.checks[name] = check

    def evaluate_conditions(self, simple_checks, conditions):
        for check in simple_checks:
            if callable(check):
                check = check()
            if not check:
                return False
        for condition, value in conditions.items():
            if not self.checks[condition](self, value):
                return False
        return True

    def register(self, settings_class=NoSwitcher, *simple_checks, **conditions):
        """
        Register a settings class with the switcher. Can be passed the settings
        class to register or be used as a decorator.

        :param settings_class: The class to register with the provided conditions.
        :param *simple_checks: A list of conditions for using the settings
                class. If any of the values are falsy, the class will not be
                used. If any of the values are callable, they will be called
                before evaluating.
        :param **conditions: Values to check. The key specifies which of the
                check functions (registered with ``add_check``) to use; the
                value is passed to the check function.
        """
        if settings_class is NoSwitcher:
            def decorator(cls):
                self.register(cls, *simple_checks, **conditions)
                return cls
            return decorator

        available_checks = self.checks.keys()
        for condition in conditions.keys():
            if condition not in available_checks:
                raise InvalidCondition('There is no check for the condition'
                        ' "%s"' % condition)

        self._registry.append((settings_class, simple_checks, conditions))

    def __call__(self):
        """
        Finds the first matching settings class from the registry, and returns
        an instance of it.
        """
        for (settings_class, simple_checks, conditions) in self._registry:
            if self.evaluate_conditions(simple_checks, conditions):
                return settings_class()
        raise NoMatchingSettings('No settings classes matched the curent'
                ' environment.')


class Switcher(BaseSwitcher):
    def __init__(self):
        super(Switcher, self).__init__()

        # Add the default checks.
        for k, v in vars(checks).items():
            match = re.match(r'^check_(\w+)$', k)
            if match and callable(v):
                self.add_check(match.group(1), v)


switcher = Switcher()
