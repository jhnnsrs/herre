import aiohttp
from oauthlib.oauth2 import WebApplicationClient
from herre.grants.oauth2.session import OAuth2Session
import logging
from herre.grants.oauth2.utils import (
    build_authorize_url,
    build_token_url,
    wait_for_redirect,
)
from .base import BaseOauth2Grant
from typing import Awaitable
from herre.types import Token
from typing import Protocol, runtime_checkable

logger = logging.getLogger(__name__)
REDIRECT_PORT = 6767


@runtime_checkable
class RedirectWaiter(Protocol):
    def __call__(
        self,
        starturl,
        redirect_host="localhost",
        redirect_port=6767,
        path="/",
        timeout=400,
    ) -> Awaitable[str]:
        ...


class AuthorizationCodeServerGrant(BaseOauth2Grant):
    redirect_port: int = 6767
    redirect_timeout: int = 40
    redirect_host: str = "localhost"
    redirect_waiter: RedirectWaiter = wait_for_redirect
    """ A simple webserver that will listen for a redirect from the OSF and return the path """

    async def afetch_token(self, force_refresh=True) -> Token:
        web_app_client = WebApplicationClient(
            self.client_id.get_secret_value(),
            scope=self.scope_delimiter.join(self.scopes + ["openid"]),
        )

        # Create an OAuth2 session for the OSF
        async with OAuth2Session(
            self.client_id.get_secret_value(),
            web_app_client,
            scope=self.scope_delimiter.join(self.scopes + ["openid"]),
            redirect_uri=f"http://{self.redirect_host}:{self.redirect_port}/",
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
        ) as session:
            auth_url, state = session.authorization_url(build_authorize_url(self))

            path = await self.redirect_waiter(
                auth_url,
                redirect_host=self.redirect_host,
                redirect_port=self.redirect_port,
            )

            if path:
                token_dict = await session.fetch_token(
                    build_token_url(self),
                    client_secret=self.client_secret.get_secret_value(),
                    authorization_response=path,
                    state=state,
                )

                return Token(**token_dict)

        raise Exception("Could not fetch token")
