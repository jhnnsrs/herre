import asyncio
from optparse import Option
from re import L
from typing import List, Optional
import aiohttp
from pydantic import BaseModel, Field, SecretStr
from herre.errors import LoginException
from herre.grants.base import BaseGrant
import os
import logging
from herre.types import User, Token
import shelve
import contextvars
import os
from koil import koilable, Koil
from koil.composition import KoiledModel
from koil.helpers import unkoil

current_herre = contextvars.ContextVar("current_herre")

logger = logging.getLogger(__name__)


class Herre(KoiledModel):
    grant: Optional[BaseGrant] = None
    base_url: str = ""
    client_id: SecretStr = SecretStr("")
    client_secret: SecretStr = SecretStr("")
    scopes: List[str] = Field(default_factory=lambda: list(["introspection"]))
    authorize_path: str = "authorize"
    refresh_path: str = "token"
    token_path: str = "token"
    append_trailing_slash = True
    token_file: str = "token.temp"
    userinfo_path: str = "userinfo"
    max_retries: int = 1
    allow_insecure: bool = False
    scope_delimiter: str = " "

    login_on_enter: bool = False
    logout_on_exit: bool = False

    no_temp: bool = False

    _lock: asyncio.Lock = None
    _user: Optional[User] = None
    _token: Optional[Token] = None

    @property
    def user(self) -> User:
        assert (
            self._lock is not None
        ), "Please enter the context first to access this variable"
        assert hasattr(
            self.grant, "afetch_user"
        ), "Grant is not a user grant. You are not identifier by a user."
        assert self._user is not None, "No user fetched"
        return self._user

    @property
    def token(self) -> Token:
        assert (
            self._lock is not None
        ), "Please enter the context first to access this variable"
        assert self._token is not None, "No token fetched"
        return self._token

    async def aget_token(self):
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
            if not self._token or not self._token.access_token:
                await self.alogin()

        return self._token.access_token

    async def alogin(self, force_refresh=False, retry=0):
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

        potential_user = None
        potential_token = None

        if not force_refresh and not self.no_temp:
            try:
                with shelve.open(self.token_file) as cfg:
                    client_id = cfg["client_id"]
                    if client_id == self.client_id.get_secret_value():
                        potential_token = Token(**cfg["token"])
                        if "user" in cfg:
                            potential_user = User(**cfg["user"])
                    else:
                        logger.info(
                            "Ommiting token file as client_id does not match current client_id"
                        )

            except Exception:
                print
                logger.info("No token file found")

        if not potential_token or force_refresh:
            potential_token = await self.grant.afetch_token(self)

        if not potential_user or force_refresh:
            if hasattr(self.grant, "afetch_user"):
                potential_user = await self.grant.afetch_user(self, potential_token)

        if not self.no_temp:
            with shelve.open(self.token_file, "w") as cfg:
                cfg["client_id"] = self.client_id.get_secret_value()
                cfg["token"] = potential_token.dict()
                if potential_user:
                    cfg["user"] = potential_user.dict()

        self._token = potential_token
        self._user = potential_user

    async def alogout(self):
        assert (
            self._lock is not None
        ), "We were not initialized. Please enter the context first"

        try:
            with shelve.open(self.token_file) as cfg:
                cfg["token"] = None
                cfg["user"] = None
                cfg["client_id"] = None
        except KeyError:
            pass

        self.state = None

    def login(self, force_refresh=False, retry=0, **kwargs):
        return unkoil(
            self.alogin,
            force_refresh=force_refresh,
            retry=retry,
            **kwargs,
        )

    def get_token(self, *args, **kwargs):
        return unkoil(self.aget_token, *args, **kwargs)

    def logout(self, **kwargs):
        return unkoil(self.alogout, **kwargs)

    @property
    def logged_in(self):
        return self.state is not None

    async def __aenter__(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0" if self.allow_insecure else "1"
        self._lock = asyncio.Lock()
        current_herre.set(self)
        if self.login_on_enter:
            await self.alogin()
        return self

    async def __aexit__(self, *args, **kwargs):
        if self.logout_on_exit:
            await self.alogout()
        current_herre.set(None)

    class Config:
        underscore_attrs_are_private = True
        extra = "forbid"


def build_userinfo_url(herre: Herre):
    return (
        f"{herre.base_url}/{herre.userinfo_path}/"
        if herre.append_trailing_slash
        else f"{herre.base_url}/{herre.userinfo_path}"
    )
