from herre.grants.base import BaseGrant
from herre.grants.refreshable import Refreshable
from oauthlib.oauth2.rfc6749.clients.backend_application import BackendApplicationClient
from herre.grants.session import OAuth2Session
from herre.grants.utils import build_token_url
from herre.herre import Herre
from herre.types import Token


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
