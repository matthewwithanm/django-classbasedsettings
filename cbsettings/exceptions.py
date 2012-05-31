class SettingsFactoryDoesNotExist(Exception):
    pass


class InvalidSettingsFactory(Exception):
    pass


class NoMatchingSettings(Exception):
    """Raised when a suitable settings class cannot be found."""
    pass


class InvalidCondition(Exception):
    pass
