import aiohttp
from herre.grants.base import BaseGrant
from herre.grants.refreshable import Refreshable
from oauthlib.oauth2 import WebApplicationClient
from herre.grants.session import OAuth2Session
from herre.types import Token, User
import webbrowser
from aiohttp import web
import asyncio
import logging
from herre.grants.utils import build_authorize_url, build_me_url, build_token_url
from herre.herre import Herre
from herre.utils import wait_for_redirect

logger = logging.getLogger(__name__)
REDIRECT_PORT = 6767


class AuthorizationCodeServerGrant(BaseGrant, Refreshable):
    redirect_port: int = 6767
    redirect_timeout: int = 40
    redirect_host: str = "localhost"

    async def afetch_token(self, herre: Herre) -> Token:

        web_app_client = WebApplicationClient(
            herre.client_id.get_secret_value(),
            scope=herre.scope_delimiter.join(herre.scopes + ["openid"]),
        )

        # Create an OAuth2 session for the OSF
        async with OAuth2Session(
            herre.client_id.get_secret_value(),
            web_app_client,
            scope=herre.scope_delimiter.join(herre.scopes + ["openid"]),
            redirect_uri=f"http://{self.redirect_host}:{self.redirect_port}/",
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
        ) as session:

            auth_url, state = session.authorization_url(build_authorize_url(herre))

            path = await self.get_path_from_redirect(auth_url)

            if path:
                token_dict = await session.fetch_token(
                    build_token_url(herre),
                    client_secret=herre.client_secret.get_secret_value(),
                    authorization_response=path,
                    state=state,
                )

                return Token(**token_dict)

        raise Exception("Could not fetch token")

    async def afetch_user(self, herre: Herre, token: Token) -> User:
        async with aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {token.access_token}"},
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
        ) as session:
            async with session.get(build_me_url(herre)) as resp:

                user_json = await resp.json()
                if "detail" in user_json:
                    raise Exception(user_json["detail"])

                return User(**user_json)

    async def get_path_from_redirect(self, auth_url):
        return await wait_for_redirect(
            auth_url, redirect_host="localhost", redirect_port=self.redirect_port
        )
