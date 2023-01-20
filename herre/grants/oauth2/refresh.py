from .base import BaseOauth2Grant
from herre.grants.base import BaseGrant
import aiohttp
import ssl
from typing import Optional, Union
from herre.types import Token
from .utils import build_refresh_url
import logging

logger = logging.getLogger(__name__)


async def arefresh(
    resfresh_url: str,
    client_id: str,
    client_secret: str,
    refresh_token: str,
    ssl_context: Optional[ssl.SSLContext] = None,
) -> Token:
    """Refreshes a token on the given url with the given client_id and client_secret

    Args:
        resfresh_url (str): The url to refresh the token on
        client_id (str): The client_id to use
        client_secret (str): The client_secret to use
        refresh_token (str): The refresh_token to use
        ssl_context (Optional[ssl.SSLContext], optional): Specific SSL token to use. Defaults to None.

    Returns:
        Oauth2Token: The refreshed token
    """
    assert refresh_token, "Token had not refresh-token attached"
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context) if ssl_context else None
    ) as session:
        async with session.post(
            resfresh_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
        ) as resp:
            token = await resp.json()
            return Token(**token)


class RefreshGrant(BaseGrant):
    """Tries to refresh the token (if it is not expired)
    and a refresh token is available. When the token is expired
    and no refresh token is available, it will try to fetch a new token.

    This grant does not refresh the token automatically. Only when it is
    implicitly called by the Herre api.

    You can choose autofresh grant to refresh the token automatically.

    Args:
        BaseGrant (_type_): _description_
    """

    grant: BaseOauth2Grant

    _token: Optional[Token] = None

    async def afetch_token(self, force_refresh: bool = False) -> Token:
        """Fetches a token from the oauth2 provider.

        Args:
            force_refresh (bool, optional): Force a refresh of the token. Defaults to False.

        Returns:
            Token: The token
        """
        if not force_refresh:
            if self._token and not self._token.is_expired():
                return self._token

            if self._token and self._token.refresh_token:
                try:
                    assert (
                        self._token.refresh_token
                    ), "Token had not refresh-token attached"
                    self._token = await arefresh(
                        resfresh_url=build_refresh_url(self.grant),
                        client_id=self.grant.client_id.get_secret_value(),
                        client_secret=self.grant.client_secret.get_secret_value(),
                        refresh_token=self._token.refresh_token,
                        ssl_context=self.grant.ssl_context,
                    )
                    return self._token
                except Exception as e:
                    logger.debug("Could not refresh token. Fetching new one")
                    pass

        self._token = await self.grant.afetch_token(force_refresh=force_refresh)
        return self._token
