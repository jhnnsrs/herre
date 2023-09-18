import asyncio
from typing import Optional, TypeVar
from herre.errors import HerreError
from herre.grants.base import BaseGrant
import os
import logging
from herre.types import Token, TokenRequest
import contextvars
from koil.composition import KoiledModel
from koil.helpers import unkoil
from herre.fetcher.types import UserFetcher
from pydantic import BaseModel

current_herre: contextvars.ContextVar["Herre"] = contextvars.ContextVar("current_herre")

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Herre(KoiledModel):
    """Herre is a client for Token authentication.

    It provides a unified, composable interface for token based authentication based on grant.
    A grant is a class that is able to retrieve a token. Importantly grants do not have to
    directly call the token endpoint. They can also use a cache or other means to retrieve the
    token.

    Herre is a context manager. This allows it both to provide itself as a singleton and handle
    the asynchronous interface of the grant. As well as providing a lock to ensure that only one
    request is happening at a time.

    Example:
        ```python
        from herre import Herre,
        from herre.grants.oauth2.client_credentials import ClientCredentialsGrant

        herre = Herre(
            grant=ClientCredentialsGrant(
                client_id="my_client_id",
                client_secret="my_client
                base_url="https://my_token_url",
            )
        )

        with herre:
            token = herre.get_token()
        ```

        or aync

        ```python
        from herre import Herre,
        from herre.grants.oauth2.client_credentials import ClientCredentialsGrant

        herre = Herre(
            grant=ClientCredentialsGrant(
                client_id="my_client_id",
                client_secret="my_client
                base_url="https://my_token_url",
            )
        )

        async with herre:
            token = await herre.get_token()
        ```

    """

    grant: BaseGrant
    fetcher: Optional[UserFetcher] = None
    max_retries: int = 1
    allow_insecure: bool = False
    scope_delimiter: str = " "
    auto_login = True

    login_on_enter: bool = False
    logout_on_exit: bool = False
    entered = False

    no_temp: bool = False

    _lock: Optional[asyncio.Lock] = None
    _token: Optional[Token] = None

    @property
    def token(self) -> Token:
        "The current token"
        assert (
            self._lock is not None
        ), "Please enter the context first to access this variable"
        assert self._token is not None, "No token fetched"
        return self._token

    async def aget_token(self, **kwargs) -> str:
        """Get an access token

        Will return an access token if it is already available or
        try to login depending on auto_login. The checking and potential retrieving will happen
        in a lock ensuring that not multiple requests are happening at the same time.

        Args:
            auto_login (bool, optional): Should we allow an automatic login. Defaults to True.

        Returns:
            str:  The access token
        """
        assert (
            self._lock is not None
        ), "We were not initialized. Please enter the context first"

        async with self._lock:
            if not self._token or not self._token.access_token:
                await self.arequest_from_grant(TokenRequest(context=kwargs))

        assert self._token is not None, "We should have a token by now"
        return self._token.access_token

    async def arefresh_token(self, **kwargs) -> str:
        """Refresh the token

        Will cause the linked grant to refresh the token. Depending
        on the link logic, this might cause another login.

        """

        async with self._lock:
            return await self.arequest_from_grant(
                TokenRequest(is_refresh=True, context=kwargs)
            )

    async def arequest_from_grant(self, request: TokenRequest) -> Token:
        print("arequest_from_grant", request)
        potential_token = await self.grant.afetch_token(request)
        self._token = potential_token
        return self._token

    def get_token(self, **kwargs) -> str:
        """Get an access token

        Will return an access token if it is already available or
        try to login depending on auto_login. The checking and potential retrieving will happen
        in a lock ensuring that not multiple requests are happening at the same time.
        """
        return unkoil(self.aget_token, **kwargs)

    async def aget_user(self) -> BaseModel:  # TODO: Should be generic
        """Get the current user

        Will return the current user if a fetcher is available
        """
        assert (
            self._lock is not None
        ), "We were not initialized. Please enter the context first"
        assert self.fetcher is not None, "We have no fetcher available"
        token = await self.aget_token()
        return await self.fetcher.afetch_user(token)

    async def __aenter__(self):
        """Enters the context and logs in if needed"""
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0" if self.allow_insecure else "1"
        self._lock = asyncio.Lock()
        current_herre.set(self)
        if self.login_on_enter:
            await self.alogin()
        self.entered = True
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """Exits the context and logs out if needed"""
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
        if self.logout_on_exit:
            await self.alogout()
        current_herre.set(None)

    def _repr_html_inline_(self) -> str:
        """Jupyter inline representation"""
        return f"<table><tr><td>auto_login</td><td>{self.auto_login}</td></tr></table>"

    class Config:
        underscore_attrs_are_private = True
        extra = "forbid"
