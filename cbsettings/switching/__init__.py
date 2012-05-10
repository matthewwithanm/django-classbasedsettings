from django.utils.datastructures import SortedDict
import re
from ..exceptions import AlreadyRegistered, InvalidCondition, NoMatchingSettings
from . import checks


class NoSwitcher:
    """Used as a sentinel argument for Switcher.register"""
    pass


class Switcher(object):
    checks = {}

    def __init__(self):
        self._registry = []

    def add_check(self, name, check):
        """Adds a checking function to the switcher."""
        self.checks[name] = check

    def evaluate_conditions(self, simple_checks, conditions):
        for check in simple_checks:
            if not check():
                return False
        for condition, value in conditions.items():
            if not self.checks[condition](self, value):
                return False
        return True

    def register(self, settings_class=NoSwitcher, *simple_checks, **conditions):
        """
        Register a settings class with the switcher. Can be passed the settings
        class to register or be used as a decorator.
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


switcher = Switcher()

for k, v in vars(checks).items():
    match = re.match(r'^check_(\w+)$', k)
    if match and callable(v):
        switcher.add_check(match.group(1), v)
