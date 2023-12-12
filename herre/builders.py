from herre import Herre
from typing import Optional, List
from herre.grants.oauth2.authorization_code import AuthorizationCodeGrant
from herre.grants.oauth2.redirecters import AioHttpServerRedirecter


def github_desktop(
    client_id: str, client_secret: str, scopes: Optional[List[str]] = None
) -> Herre:
    """Creates a Herre instance that can be used to login locally to github

    This function will create a Herre instance that can be used to login locally to github.
    It will use the authorization code grant, and a aiohttp server redirecter.

    Parameters
    ----------
    client_id : str
        The client id to use
    client_secret : str
        The client secret to use
    scopes : Optional[List[str]], optional
        The scopes to use, by default None

    Returns
    -------
    Herre
        The Herre instance
    """
    if scopes is None:
        scopes = []

    return Herre(
        grant=AuthorizationCodeGrant(
            base_url="https://github.com/login/oauth",
            token_path="access_token",
            client_id=client_id,  # type: ignore
            client_secret=client_secret,  # type: ignore
            scopes=scopes,
            redirecter=AioHttpServerRedirecter(),
            append_trailing_slash=False,  # github does not like trailing slashes
        )
    )
