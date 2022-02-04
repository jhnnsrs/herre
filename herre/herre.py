from typing import Optional
import aiohttp
from herre.errors import NoHerreFound
from herre.grants.base import BaseGrant
import os
import logging
from herre.types import HerreState, User
import shelve
import contextvars
import os
from koil.loop import koil


current_herre = contextvars.ContextVar("current_herre", default=None)
GLOBAL_HERRE = None


logger = logging.getLogger(__name__)


def set_current_herre(herre, set_global=True):
    global GLOBAL_HERRE
    current_herre.set(herre)
    if set_global:
        GLOBAL_HERRE = herre


def set_global_herre(herre):
    global GLOBAL_HERRE
    GLOBAL_HERRE = herre


def get_current_herre(allow_global=True):
    global GLOBAL_HERRE
    herre = current_herre.get()

    if not herre:
        if not allow_global:
            raise NoHerreFound(
                "No current herre found and global herre are not allowed"
            )
        if not GLOBAL_HERRE:
            if os.getenv("HERRE_ALLOW_FAKTS_GLOBAL", "True") == "True":
                try:
                    from herre.fakts import FaktsHerre

                    GLOBAL_HERRE = FaktsHerre()
                    return GLOBAL_HERRE
                except ImportError as e:
                    raise NoHerreFound("Error creating Fakts Herre") from e
            else:
                raise NoHerreFound(
                    "No current herre found and and no global herre found"
                )

        return GLOBAL_HERRE

    return herre


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
        token_path="token",
        authorize_path="authorize",
        refresh_path="token",
        append_trailing_slash=True,
        token_file="token.temp",
        userinfo_path="userinfo",
        max_retries=1,
        allow_insecure=False,
        no_temp=False,
        register_global=True,
        **kwargs,
    ) -> None:
        """Creates A Herre Client

        Args:
            config_path (str, optional): [description]. Defaults to "bergen.yaml".
            username (str, optional): [description]. Defaults to None.
            password (str, optional): [description]. Defaults to None.
            allow_insecure (bool, optional): [description]. Defaults to False.
            in_sync (bool, optional): Should we force an in_sync modus if an event loop is already running. Loop will be send to another thread. Defaults to True.

        Raises:
            HerreError: [description]
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
        self.token_path = token_path
        self.refresh_path = refresh_path
        self.userinfo_path = userinfo_path
        self.append_trailing_slash = append_trailing_slash
        self.token_file = token_file
        self.no_temp = no_temp

        self.state: HerreState = None

        super().__init__(*args, **kwargs)
        if register_global:
            set_global_herre(self)

    async def aget_token(self):
        if not self.state or not self.state.access_token:
            await self.alogin()

        return self.state.access_token

    async def alogin(self, force_relogin=False, retry=0, **kwargs) -> HerreState:

        if retry > self.max_retries:
            raise Exception("Exceeded Login Retries")

        if not force_relogin and not self.no_temp:
            try:
                with shelve.open(self.token_file) as cfg:
                    client_id = cfg["client_id"]
                    if client_id == self.client_id:
                        self.state = HerreState(**cfg["state"])
                    else:
                        logger.info("Omitting old token")

            except Exception:
                pass

        if not self.state:
            token_dict = await self.grant.afetch_token(self, **kwargs)
            print(f"Grant fetched token {token_dict}")
            self.state = HerreState(
                **token_dict, client_id=self.client_id, scopes=self.requested_scopes
            )

        try:
            user_info_endpoint = build_userinfo_url(self)
            async with aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.state.access_token}"}
            ) as session:
                async with session.get(user_info_endpoint) as resp:
                    user_json = await resp.json()
                    print(user_json)
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
            logger.error(f"Token Invalid {e}")
            self.state = None
            await self.alogin(force_relogin=True, retry=retry + 1, **kwargs)

        return self.state

    async def alogout(self):
        if self.grant:
            return await self.grant.alogout()

        try:
            with shelve.open(self.token_file) as cfg:
                cfg["state"] = None
                cfg["client_id"] = None
        except KeyError:
            pass

        self.state = None

    async def arefresh(self):
        return await self.grant.alogin()

    def login(self, **kwargs):
        return koil(self.alogin(), **kwargs)

    def logout(self, **kwargs):
        return koil(self.alogout(), **kwargs)

    def refresh(self):
        return koil(self.arefresh())

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


def build_userinfo_url(herre: Herre):
    return (
        f"{herre.base_url}/{herre.userinfo_path}/"
        if herre.append_trailing_slash
        else f"{herre.base_url}/{herre.userinfo_path}"
    )
