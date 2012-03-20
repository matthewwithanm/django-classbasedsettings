class SettingsFactoryDoesNotExist(Exception):
    pass


class InvalidSettingsFactory(Exception):
    pass


class AlreadyRegistered(Exception):
    """Raised when a settings class has already been registered."""
    pass


class NoMatchingSettings(Exception):
    """Raised when a suitable settings class cannot be found."""
    pass


class InvalidCondition(Exception):
    pass
