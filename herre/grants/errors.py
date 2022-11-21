from herre.errors import HerreError


class GrantException(HerreError):
    """Base class for all grant exceptions"""

    pass


class RetriesExceededException(GrantException):
    """Raised when a grant exceeds the number of retries"""

    pass
