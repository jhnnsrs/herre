import asyncio
from typing import Optional, TypeVar
from herre.errors import HerreError, NoHerreFound
from herre.grants.base import BaseGrant
import os
import logging
from herre.models import Token, TokenRequest
import contextvars
from koil.composition import KoiledModel
from koil.helpers import unkoil
from herre.fetcher.models import UserFetcher
from pydantic import BaseModel

current_herre: contextvars.ContextVar[Optional["Herre"]] = contextvars.ContextVar(
    "current_herre", default=None
)

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
        assert (
            self._lock is not None
        ), "We were not initialized. Please enter the context first"

        async with self._lock:
            await self.arequest_from_grant(
                TokenRequest(is_refresh=True, context=kwargs)
            )
            assert self._token is not None, "We should have a token by now"
            return self._token.access_token

    async def arequest_from_grant(self, request: TokenRequest) -> Token:
        """Request a token from the grant

        You should not need to call this method directly. It is used internally
        to request a token from the grant, and will not directly acquire a lock
        (so multiple requests can happen at the same time, which is often not what
        you want).

        Parameters
        ----------
        request : TokenRequest
            The token request (contains context and whether it is a refresh request)

        Returns
        -------
        Token
            The token (with access_token, refresh_token, etc.)
        """
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

    async def aget_user(self, **kwargs) -> BaseModel:  # TODO: Should be generic
        """Get the current user

        Will return the current user if a fetcher is available
        """
        assert (
            self._lock is not None
        ), "We were not initialized. Please enter the context first"
        assert self.fetcher is not None, "We have no fetcher available"
        if not self._token:
            raise HerreError("No token available")
        async with self._lock:
            if not self._token or not self._token.access_token:
                await self.arequest_from_grant(TokenRequest(context=kwargs))

        assert self._token is not None, "We should have a token by now"
        return await self.fetcher.afetch_user(self._token)

    async def __aenter__(self) -> "Herre":
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
        """Pydantic config"""

        underscore_attrs_are_private = True
        extra = "forbid"


def get_current_herre() -> Herre:
    """Get the current herre instance"""
    herre = current_herre.get()

    if herre is None:
        raise NoHerreFound("No herre instance available")

    return herre
