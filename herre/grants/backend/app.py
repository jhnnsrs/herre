from herre.grants.base import DefaultGrant
from oauthlib.oauth2.rfc6749.clients.backend_application import BackendApplicationClient
from herre.grants.session import OAuth2Session

from herre.grants.registry import register_grant
from herre.config import GrantType


class BackendGrant(DefaultGrant):
    refreshable = True

    async def afetch_token(self, **kwargs):
        auth_client = BackendApplicationClient(
            client_id=self.client_id, scope=" ".join(self.scopes)
        )

        async with OAuth2Session(client=auth_client, scope=self.scope) as session:
            token = await session.fetch_token(
                token_url=self.token_url,
                client_id=self.client_id,
                client_secret=self.client_secret,
                verify=True,
            )

        return token
