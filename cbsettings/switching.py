from django.utils.datastructures import SortedDict
import socket
from .exceptions import AlreadyRegistered, InvalidCondition, NoMatchingSettings


class NoSwitcher:
    """Used as a sentinel argument for Switcher.register"""
    pass


class Switcher(object):
    checks = dict(
        hostnames=lambda sw, val: socket.gethostname() in val,
    )

    def __init__(self):
        self._registry = SortedDict()

    def evaluate_conditions(self, conditions):
        for condition, value in conditions.items():
            if not self.checks[condition](self, value):
                return False
        return True

    def register(self, settings_class=NoSwitcher, **conditions):
        """
        Register a settings class with the switcher. Can be passed the settings
        class to register or be used as a decorator.
        """
        if settings_class is NoSwitcher:
            def decorator(cls):
                self.register(cls, **conditions)
                return cls
            return decorator

        if settings_class in self._registry:
            raise AlreadyRegistered('The settings class "%s" is already'
                    ' registered.')

        available_checks = self.checks.keys()
        for condition in conditions.keys():
            if condition not in available_checks:
                raise InvalidCondition('There is no check for the condition'
                        ' "%s"' % condition)

        self._registry[settings_class] = conditions

    def __call__(self):
        """
        Finds the first matching settings class from the registry, and returns
        an instance of it.
        """
        for settings_class, conditions in self._registry.items():
            if self.evaluate_conditions(conditions):
                return settings_class()
        raise NoMatchingSettings('No settings classes matched the curent'
                ' environment.')


switcher = Switcher()
