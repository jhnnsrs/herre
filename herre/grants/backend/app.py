from herre.grants.refreshable import RefreshableGrant
from oauthlib.oauth2.rfc6749.clients.backend_application import BackendApplicationClient
from herre.grants.session import OAuth2Session

from herre.grants.registry import register_grant
from herre.config import GrantType
from herre.grants.utils import build_token_url
from herre.herre import Herre


class BackendGrant(RefreshableGrant):
    refreshable = True

    async def afetch_token(self, herre: Herre, **kwargs):
        auth_client = BackendApplicationClient(
            client_id=herre.client_id, scope=" ".join(herre.requested_scopes)
        )

        async with OAuth2Session(client=auth_client, scope=herre.scope) as session:
            print(build_token_url(herre))

            token = await session.fetch_token(
                token_url=build_token_url(herre),
                client_id=herre.client_id,
                client_secret=herre.client_secret,
                verify=True,
            )

        return token
