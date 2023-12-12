import aiohttp
from herre.grants.oauth2.base import BaseOauth2Grant
from herre.models import Token, TokenRequest

from oauthlib.oauth2.rfc6749.clients.backend_application import BackendApplicationClient

from herre.grants.oauth2.utils import build_token_url
from oauthlib.common import urldecode


class ClientCredentialsGrant(BaseOauth2Grant):
    """A grant that uses the client credentials flow"""

    async def afetch_token(self, request: TokenRequest) -> Token:
        """Fetches a token

        This function will fetch a token from the oauth2 provider,
        using the client credentials flow.


        Parameters
        ----------
        request : TokenRequest
            The token request to use

        Returns
        -------
        Token
            The token
        """
        scope = self.scope_delimiter.join(self.scopes)

        auth_client = BackendApplicationClient(
            client_id=self.client_id.get_secret_value(),
            scope=self.scope_delimiter.join(self.scopes),
        )

        token_url = build_token_url(self)

        body = auth_client.prepare_request_body(
            client_secret=self.client_secret.get_secret_value(),
            client_id=self.client_id.get_secret_value(),
        )

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }

        data = dict(urldecode(body))

        # Create an OAuth2 session for the OSF
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=self.ssl_context)
            if self.ssl_context
            else None,
            headers=headers,
        ) as session:
            async with session.post(
                token_url,
                data=data,
                auth=aiohttp.BasicAuth(
                    self.client_id.get_secret_value(),
                    self.client_secret.get_secret_value(),
                ),
            ) as resp:
                text = await resp.text()

                auth_client.parse_request_body_response(text, scope=scope)

                token = auth_client.token
                return Token(**token)
