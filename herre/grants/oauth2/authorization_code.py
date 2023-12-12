import aiohttp
from oauthlib.oauth2 import WebApplicationClient
import logging
from herre.grants.oauth2.utils import (
    build_authorize_url,
    build_token_url,
)
from .base import BaseOauth2Grant
from typing import Awaitable
from herre.models import Token, TokenRequest
from typing import Protocol, runtime_checkable
from oauthlib.common import generate_token, urldecode


logger = logging.getLogger(__name__)


@runtime_checkable
class Redirecter(Protocol):
    """A protocol for a from oauthlib.common import generate_tokenedirect waiter"""

    async def aget_redirect_uri(self, token_request: TokenRequest) -> str:
        """Retrieves the redirect uri

        This function will retrieve the redirect uri from the RedirectWaiter.
        This function has to be implemented by the user.

        """

    def astart(
        self,
        starturl: str,
    ) -> Awaitable[str]:
        """Awaits a redirect

        This has to be implemented by a user, and should
        return the path of the redirect (with the code)

        Parameters
        ----------
        starturl : str
            The url to start the redirect from

        Returns
        -------
        Awaitable[str]
            The path of the redirect (with the code)

        """
        ...


class AuthorizationCodeGrant(BaseOauth2Grant):
    """A grant that uses the authorization code flow

    This grant will create an AuthorizationCodeGrant, and use it to fetch a token.



    """

    redirecter: Redirecter
    """ A simple webserver that will listen for a redirect from the OSF and return the path """

    async def afetch_token(self, request: TokenRequest) -> Token:
        """Fetch Token

        This function will fetch a token from the oauth2 provider,
        using the authorization code flow. It will retrieve the redirect_uri from the redirecter,
        and use that as the redirect_uri, it will then build an authorization url, and delegate the
        redirect to the RedirectWaiter. When the redirecter has received the redirect, it will
        return the code to this function, which will then use the code to fetch a token.


        Parameters
        ----------
        request : TokenRequest
            The token request to use

        Returns
        -------
        Token
            The token
        """

        state = generate_token()
        scope = self.scope_delimiter.join(self.scopes)
        redirect_uri = await self.redirecter.aget_redirect_uri(request)

        web_app_client = WebApplicationClient(
            self.client_id.get_secret_value(),
            scope=scope,
        )

        auth_url = web_app_client.prepare_request_uri(
            build_authorize_url(self),
            redirect_uri=redirect_uri,
            scope=scope,
            state=state,
        )

        web_app_client = WebApplicationClient(
            self.client_id.get_secret_value(),
            scope=self.scope_delimiter.join(self.scopes),
        )

        authorization_response = await self.redirecter.astart(
            auth_url,
        )

        web_app_client.parse_request_uri_response(
            str(authorization_response), state=state
        )
        code = web_app_client.code

        token_url = build_token_url(self)

        body = web_app_client.prepare_request_body(
            code=code,
            redirect_uri=redirect_uri,
            client_secret=self.client_secret.get_secret_value(),
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
            async with session.request(
                "POST",
                token_url,
                data=data,
            ) as resp:
                text = await resp.text()

                web_app_client.parse_request_body_response(text, scope=scope)

                token = web_app_client.token
                return Token(**token)
