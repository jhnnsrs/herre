import aiohttp
from herre.grants.base import BaseGrant
from herre.grants.refreshable import Refreshable
from oauthlib.oauth2.rfc6749.clients.backend_application import BackendApplicationClient
from herre.grants.session import OAuth2Session
from herre.grants.utils import build_me_url, build_token_url, build_userinfo_url
from herre.herre import Herre
from herre.types import Token, User


class BackendGrant(BaseGrant, Refreshable):
    async def afetch_token(self, herre: Herre) -> Token:
        auth_client = BackendApplicationClient(
            client_id=herre.client_id.get_secret_value(),
            scope=herre.scope_delimiter.join(herre.scopes),
        )

        async with OAuth2Session(
            client=auth_client, scope=herre.scope_delimiter.join(herre.scopes)
        ) as session:

            token_dict = await session.fetch_token(
                token_url=build_token_url(herre),
                client_id=str(herre.client_id.get_secret_value()),
                client_secret=str(herre.client_secret.get_secret_value()),
                verify=True,
            )

        return Token(**token_dict)

    async def afetch_user(self, herre: Herre, token: Token) -> User:
        async with aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {token.access_token}"}
        ) as session:
            async with session.get(build_me_url(herre)) as resp:

                user_json = await resp.json()
                if "detail" in user_json:
                    raise Exception(user_json["detail"])

                return User(**user_json)
