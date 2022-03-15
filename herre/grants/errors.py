class GrantException(Exception):
    pass


class RetryException(GrantException):
    pass


class NoUserException(GrantException):
    pass
