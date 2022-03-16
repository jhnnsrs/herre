from herre.grants.base import BaseGrant
from herre.grants.openid import OpenIdUser
from herre.grants.refreshable import Refreshable
from oauthlib.oauth2 import WebApplicationClient
from herre.grants.session import OAuth2Session
from herre.types import Token, User
import webbrowser
from aiohttp import web
import asyncio
import logging
from herre.grants.utils import build_authorize_url, build_token_url
from herre.herre import Herre
from herre.utils import wait_for_redirect

logger = logging.getLogger(__name__)
REDIRECT_PORT = 6767


class AuthorizationCodeServerGrant(BaseGrant, Refreshable, OpenIdUser):
    def __init__(
        self,
        redirect_port=REDIRECT_PORT,
        redirect_timeout=40,
    ) -> None:
        self.redirect_port = redirect_port
        self.redirect_timeout = redirect_timeout
        self.redirect_uri = f"http://localhost:{redirect_port}/"

    async def afetch_token(self, herre: Herre) -> Token:

        web_app_client = WebApplicationClient(
            herre.client_id, scope=herre.scope_delimiter.join(herre.scopes + ["openid"])
        )

        # Create an OAuth2 session for the OSF
        async with OAuth2Session(
            herre.client_id,
            web_app_client,
            scope=herre.scope_delimiter.join(herre.scopes + ["openid"]),
            redirect_uri=self.redirect_uri,
        ) as session:

            auth_url, state = session.authorization_url(build_authorize_url(herre))

            path = await self.get_path_from_redirect(auth_url)

            if path:
                token_dict = await session.fetch_token(
                    build_token_url(herre),
                    client_secret=herre.client_secret,
                    authorization_response=path,
                    state=state,
                )

                print(token_dict)
                return Token(**token_dict)

        raise Exception("Could not fetch token")

    async def get_path_from_redirect(self, auth_url):
        return await wait_for_redirect(
            auth_url, redirect_host="localhost", redirect_port=self.redirect_port
        )
