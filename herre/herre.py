import asyncio
from optparse import Option
from re import L
from typing import List, Optional
import aiohttp
import oauthlib.oauth2.rfc6749.errors
from pydantic import BaseModel, Field, SecretStr
from herre.errors import ConfigurationException, HerreError, LoginException
from herre.grants.base import BaseGrant
import os
import logging
from herre.types import Token
import shelve
import contextvars
import os
from koil import koilable, Koil
from koil.composition import KoiledModel
from koil.helpers import unkoil

current_herre: contextvars.ContextVar["Herre"] = contextvars.ContextVar("current_herre")

logger = logging.getLogger(__name__)


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
        assert (
            self._lock is not None
        ), "Please enter the context first to access this variable"
        assert self._token is not None, "No token fetched"
        return self._token

    async def aget_token(self, force_refresh: bool =False) -> str:
        """Get an access token

        This is a loop safe couroutine, that will return an access token if it is already available or
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
            if not self._token or not self._token.access_token or force_refresh:
                if not self.auto_login:
                    raise HerreError(
                        "Auto-login is set to false and we need to login again"
                    )
                await self.alogin(force_refresh=force_refresh)

        assert self._token is not None, "We should have a token by now"
        return self._token.access_token

    async def arefresh_token(self) -> str:
        return await self.aget_token(force_refresh=True)

    async def alogin(self, force_refresh:bool =False, retry: int=0) -> Token:
        """Login Function

        Login is a compount function that will try to ensure a login following the following steps:

        1. Set the current state to none (if not already set)
        2. Try to load the token from the token file (and check its validity)
        3. If the token is not valid or force_refresh is true, try to refresh the token.
        4. If the grant is a user grant (indicated on the grantclass) make a request to the userinfo endpoint and check update the state with user information
        5. Returns the state

        Args:
            force_refresh (bool, optional): [description]. Defaults to False.
            retry (int, optional): [description]. Defaults to 0.

        Raises:
            Exception: [description]
            Exception: [description]

        """
        assert (
            self._lock is not None
        ), "We were not initialized. Please enter the context first"

        potential_token = await self.grant.afetch_token(force_refresh=force_refresh)
        self._token = potential_token
        return self._token

    async def alogout(self) -> None:
        assert (
            self._lock is not None
        ), "We were not initialized. Please enter the context first"

        self._token = None

    def login(self, force_refresh:bool=False, retry: int=0) -> Token:
        return unkoil(
            self.alogin,
            force_refresh=force_refresh,
            retry=retry,
        )

    def get_token(self, force_refresh: bool =False) -> str:
        return unkoil(self.aget_token, force_refresh=force_refresh)

    def logout(self) -> None:
        return unkoil(self.alogout)

    @property
    def logged_in(self) -> bool:
        return self._token is not None

    async def __aenter__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0" if self.allow_insecure else "1"
        self._lock = asyncio.Lock()
        current_herre.set(self)
        if self.login_on_enter:
            await self.alogin()
        self.entered = True
        return self

    async def __aexit__(self, *args, **kwargs):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
        if self.logout_on_exit:
            await self.alogout()
        current_herre.set(None)

    
    def _repr_html_inline_(self):
        return f"<table><tr><td>auto_login</td><td>{self.auto_login}</td></tr></table>"

    class Config:
        underscore_attrs_are_private = True
        extra = "forbid"
