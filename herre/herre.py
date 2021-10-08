


from enum import Enum
from typing import List, Optional
from herre.config import HerreConfig
from herre.grants.code_server.app import AuthorizationCodeServerGrant
from herre.grants.backend.app import BackendGrant
from herre.grants.backend.app import BackendGrant
import os
import logging
from koil import get_current_koil, Koil
import time

from koil.loop import koil
from konfik.config.base import Config
from konfik.konfik import Konfik, get_current_konfik
from herre.grants.registry import GrantRegistry, get_current_grant_registry



logger = logging.getLogger(__name__)



class HerreError(Exception):
    pass


class Herre:

    def __init__(self,
        *args,
        register = True,
        koil: Koil = None,
        konfik: Konfik = None,
        granty_registry: GrantRegistry = None,
        **kwargs
    ) -> None:
        """ Creates A Herre Client

        Args:
            config_path (str, optional): [description]. Defaults to "bergen.yaml".
            username (str, optional): [description]. Defaults to None.
            password (str, optional): [description]. Defaults to None.
            allow_insecure (bool, optional): [description]. Defaults to False.
            in_sync (bool, optional): Should we force an in_sync modus if an event loop is already running. Loop will be send to another thread. Defaults to True.

        Raises:
            HerreError: [description]
        """
        self.konfik = konfik or get_current_konfik()
        self.grant_registry = granty_registry or get_current_grant_registry()
        self.koil = koil or get_current_koil()
        self.grant = None

        if register:
            set_current_herre(self)

        super().__init__(*args, **kwargs)




    async def alogin(self, **kwargs):
        if not self.konfik.loaded:
            await self.konfik.aload()

        self.config = HerreConfig.from_konfik(konfik=self.konfik)
        self.grant = self.grant_registry.get_grant_for_type(self.config.authorization_grant_type)(self.config, konfik=self.konfik)
        return await self.grant.alogin(**kwargs)

    async def alogout(self):
        assert self.grant, "We have never logged in"
        return await self.grant.alogin()

    async def arefresh(self):
        assert self.grant, "We have never logged in"
        return await self.grant.arefresh()


    def login(self, username: str = None, password: str = None):
        return koil(self.alogin(username=username, password=password))

    def logout(self):
        return koil(self.alogout())
    
    def refresh(self):
        return koil(self.arefresh())


    @property
    def logged_in(self):
        return self.grant and self.grant.logged_in

    @property
    def user(self):
        assert self.grant.logged_in, "User is not logged in"
        return self.grant.user

    @property
    def headers(self):
        assert self.grant.access_token is not None, "Access token is not set yet, please login?"
        return {"Authorization": f"Bearer {self.grant.access_token}"}




CURRENT_HERRE = None

def get_current_herre(**kwargs):
    global CURRENT_HERRE
    if not CURRENT_HERRE:
        CURRENT_HERRE = Herre(**kwargs)
    return CURRENT_HERRE

def set_current_herre(herre):
    global CURRENT_HERRE
    CURRENT_HERRE = herre