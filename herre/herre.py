from enum import Enum
from typing import List, Optional
import aiohttp

from pydantic.main import BaseModel
import fakts
from herre.config import HerreConfig
from herre.grants.code_server.app import AuthorizationCodeServerGrant
from herre.grants.backend.app import BackendGrant
from herre.grants.backend.app import BackendGrant
import os
import logging
from herre.types import HerreState, User
from koil import get_current_koil, Koil
import time
import shelve

from koil.loop import koil

from fakts import Fakts, get_current_fakts, Config
from herre.grants.registry import GrantRegistry, get_current_grant_registry


logger = logging.getLogger(__name__)


class HerreError(Exception):
    pass


class Herre:
    def __init__(
        self,
        *args,
        register=True,
        config: HerreConfig = None,
        fakts: Fakts = None,
        token_file="token.temp",
        userinfo_url="userinfo/",
        granty_registry: GrantRegistry = None,
        max_retries=5,
        no_temp=False,
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
        self.config = config
        self.max_retries = max_retries
        self.fakts: Fakts = fakts or get_current_fakts()
        self.grant_registry = granty_registry or get_current_grant_registry()
        self.no_temp = no_temp
        self.grant = None
        self.state: HerreState = None
        self.token_file = (
            f"{self.fakts.subapp}.{token_file}" if self.fakts.subapp else token_file
        )
        if register:
            set_current_herre(self)

        super().__init__(*args, **kwargs)

    async def alogin(self, force_relogin=False, retry=0, **kwargs) -> HerreState:
        if retry > self.max_retries:
            raise Exception("Exceeded Login Retries")
        if not self.config:
            if not self.fakts.loaded:
                await self.fakts.aload()

            self.config = await HerreConfig.from_fakts(fakts=self.fakts)

        if not force_relogin and not self.config.no_temp and not self.no_temp:
            try:
                with shelve.open(self.token_file) as cfg:
                    client_id = cfg["client_id"]
                    if client_id == self.config.client_id:
                        self.state = HerreState(**cfg["state"])
                    else:
                        logger.info("Omitting old token")

            except Exception:
                pass

        if not self.state:
            self.grant = self.grant_registry.get_grant_for_type(
                self.config.authorization_grant_type
            )(self.config, fakts=self.fakts)
            token_dict = await self.grant.afetch_token(**kwargs)
            logger.info(f"Grant fetched token {token_dict}")
            self.state = HerreState(
                **token_dict, client_id=self.config.client_id, scopes=self.config.scopes
            )

        try:
            base_url = f'{"https" if self.config.secure else "http"}://{self.config.host}:{self.config.port}{self.config.subpath}/'
            user_info_endpoint = base_url + "userinfo/"

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

                    if not self.config.no_temp:
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


CURRENT_HERRE = None


def get_current_herre(**kwargs):
    global CURRENT_HERRE
    if not CURRENT_HERRE:
        CURRENT_HERRE = Herre(**kwargs)
    return CURRENT_HERRE


def set_current_herre(herre):
    global CURRENT_HERRE
    CURRENT_HERRE = herre
