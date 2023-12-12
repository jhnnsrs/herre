class HerreError(Exception):
    """Base class for Herre errors"""

    pass


class NoHerreFound(HerreError):
    """Raised when no Herre instance is found in the context."""

    pass


class LoginException(HerreError):
    """Raised when the login dfails."""

    pass


class ConfigurationException(HerreError):
    """Raised when the configuration is invalid."""

    pass
