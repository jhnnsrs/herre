from herre.console.context import console, get_current_console
from herre.grants.base import BaseGrant
from oauthlib.oauth2.rfc6749.clients.backend_application import \
    BackendApplicationClient
from requests_oauthlib.oauth2_session import OAuth2Session

class BackendGrant(BaseGrant):
    refreshable = True

    def fetchToken(self, **kwargs):
        auth_client = BackendApplicationClient(client_id=self.config.client_id, scope=" ".join(self.config.scopes))
        oauth_session = OAuth2Session(client=auth_client, scope=self.scope)

        self.token = oauth_session.fetch_token(token_url=self.token_url, client_id=self.config.client_id,
            client_secret=self.config.client_secret, verify=True)




