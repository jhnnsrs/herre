import aiohttp
from herre.grants.oauth2.base import BaseOauth2Grant
from herre.grants.oauth2.session import OAuth2Session
from herre.types import Token
import aiohttp
from oauthlib.oauth2.rfc6749.clients.backend_application import BackendApplicationClient
from herre.grants.oauth2.session import OAuth2Session
from herre.grants.oauth2.utils import build_token_url
from herre.types import Token


class ClientCredentialsGrant(BaseOauth2Grant):
    async def afetch_token(self, force_refresh: bool = False) -> Token:
        auth_client = BackendApplicationClient(
            client_id=self.client_id.get_secret_value(),
            scope=self.scope_delimiter.join(self.scopes),
        )

        async with OAuth2Session(
            client=auth_client,
            scope=self.scope_delimiter.join(self.scopes),
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
        ) as session:

            token_dict = await session.fetch_token(
                token_url=build_token_url(self),
                client_id=str(self.client_id.get_secret_value()),
                client_secret=str(self.client_secret.get_secret_value()),
                verify=True,
            )

        return Token(**token_dict)
