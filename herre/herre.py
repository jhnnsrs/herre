import asyncio
from re import L
from typing import Optional
import aiohttp
from herre.errors import LoginException
from herre.grants.base import BaseGrant
import os
import logging
from herre.types import HerreState, User
import shelve
import contextvars
import os
from koil import koilable


current_herre = contextvars.ContextVar("current_herre")
GLOBAL_HERRE = None


logger = logging.getLogger(__name__)


@koilable(add_connectors=True)
class Herre:
    state: Optional[HerreState]

    def __init__(
        self,
        *args,
        grant: BaseGrant = None,
        base_url: str = "",
        client_id: str = "",
        client_secret: str = "",
        scopes=["introspection"],
        authorize_path="authorize",
        refresh_path="token",
        token_path="token",
        append_trailing_slash=True,
        token_file="token.temp",
        userinfo_path="userinfo",
        max_retries=1,
        allow_insecure=False,
        no_temp=False,
        register_global=True,
        **kwargs,
    ) -> None:
        """Initialize a new Herre instance.

        Will initialize a Herre instance,

        Args:
            grant (BaseGrant, optional): The Grant we use to retrieve tokens. Defaults to None.
            base_url (str, optional): The Base Url for all requests (check your openid2 connect server). Defaults to "".
            client_id (str, optional): [description]. Defaults to "".
            client_secret (str, optional): [description]. Defaults to "".
            scopes (list, optional): The  Defaults to ["introspection"].
            token_path (str, optional): [description]. Defaults to "token".
            authorize_path (str, optional): [description]. Defaults to "authorize".
            refresh_path (str, optional): [description]. Defaults to "token".
            append_trailing_slash (bool, optional): [description]. Defaults to True.
            token_file (str, optional): [description]. Defaults to "token.temp".
            userinfo_path (str, optional): [description]. Defaults to "userinfo".
            max_retries (int, optional): [description]. Defaults to 1.
            allow_insecure (bool, optional): [description]. Defaults to False.
            no_temp (bool, optional): [description]. Defaults to False.
            register_global (bool, optional): [description]. Defaults to True.
        """

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0" if allow_insecure else "1"
        self.max_retries = max_retries
        self.base_url = base_url  # is defered
        self.client_id = client_id
        self.client_secret = client_secret
        self.requested_scopes = scopes + ["openid"]
        self.scope = " ".join(self.requested_scopes)
        self.grant = grant
        self.base_url = base_url
        self.auth_path = authorize_path
        self.refresh_path = refresh_path
        self.userinfo_path = userinfo_path
        self.append_trailing_slash = append_trailing_slash
        self.token_file = token_file
        self.token_path = token_path
        self.no_temp = no_temp
        self._lock = None

        self.state: HerreState = None
        super().__init__(*args, **kwargs)

    async def aget_token(self, auto_login: bool = True):
        """Get an access token

        This is a loop safe couroutine, that will return an access token if it is already available or
        try to login depending on auto_login. THe checking and potential retrieving will happen
        in a lock ensuring that not multiple requests are happening at the same time.

        Args:
            auto_login (bool, optional): Should we allow an automatic login. Defaults to True.

        Returns:
            str:  The access token
        """
        if not self._lock:
            self._lock = asyncio.Lock()

        async with self._lock:
            if not self.state or not self.state.access_token:
                await self.alogin()

        return self.state.access_token

    async def alogin(self, force_refresh=False, retry=0, **kwargs) -> HerreState:
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

        Returns:
            HerreState: [description]
        """

        self.state = None

        if not force_refresh and not self.no_temp:
            try:
                with shelve.open(self.token_file) as cfg:
                    client_id = cfg["client_id"]
                    if client_id == self.client_id:
                        self.state = HerreState(**cfg["state"])
                    else:
                        logger.info(
                            "Ommiting token file as client_id does not match current client_id"
                        )

            except Exception:
                logger.info("No token found")

        if not self.state:
            token_dict = await self.grant.afetch_token(self, **kwargs)
            self.state = HerreState(
                **token_dict, client_id=self.client_id, scopes=self.requested_scopes
            )

        if self.grant.is_user_grant:
            try:
                user_info_endpoint = build_userinfo_url(self)
                async with aiohttp.ClientSession(
                    headers={"Authorization": f"Bearer {self.state.access_token}"}
                ) as session:
                    async with session.get(user_info_endpoint) as resp:
                        user_json = await resp.json()
                        if "detail" in user_json:
                            raise Exception(user_json["detail"])

                        try:
                            self.state.user = User(**user_json)
                        except:
                            self.state.user = None

                        if not self.no_temp:
                            with shelve.open(self.token_file) as cfg:
                                cfg["client_id"] = self.state.client_id
                                cfg["state"] = self.state.dict()

            except Exception as e:
                if retry > self.max_retries:
                    raise LoginException("Exceeded Login Retries") from e
                await self.alogin(force_refresh=True, retry=retry + 1, **kwargs)

        else:
            self.state.user = None

        return self.state

    async def alogout(self):

        try:
            with shelve.open(self.token_file) as cfg:
                cfg["state"] = None
                cfg["client_id"] = None
        except KeyError:
            pass

        self.state = None

    def login(self, force_refresh=False, retry=0, **kwargs):
        return koil(
            self.alogin(
                force_refresh=force_refresh,
                retry=retry,
            ),
            **kwargs,
        )

    def logout(self, **kwargs):
        return koil(self.alogout(), **kwargs)

    @property
    def logged_in(self):
        return self.state is not None

    @property
    def user(self):
        assert self.state, "We are not yet logged in"
        assert self.state.user, "Login is not associated with a user"
        return self.state.user

    @property
    def scopes(self):
        assert self.state, "We are not yet logged in"
        assert self.state.scopes, "Login is not associated with a user"
        return self.state.scopes

    @property
    def headers(self):
        assert self.state, "We are not yet logged in"
        return {"Authorization": f"Bearer {self.state.access_token}"}

    async def __aenter__(self):
        current_herre.set(self)
        return self

    async def __aexit__(self, *args, **kwargs):
        current_herre.set(None)


def build_userinfo_url(herre: Herre):
    return (
        f"{herre.base_url}/{herre.userinfo_path}/"
        if herre.append_trailing_slash
        else f"{herre.base_url}/{herre.userinfo_path}"
    )
