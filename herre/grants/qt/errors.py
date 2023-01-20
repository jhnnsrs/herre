from herre.grants.errors import GrantException


class UserCancelledError(GrantException):
    """Invoked when the user cancels the login process"""

    pass
