from herre.grants.errors import GrantException


class Oauth2RedirectError(GrantException):
    """Raised when a grant fails to redirect"""

    pass


class Oauth2TimeoutError(GrantException):
    """Raised when a grant times out"""

    pass
