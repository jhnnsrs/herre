


from enum import Enum
from typing import List, Optional
import fakts
from herre.config import HerreConfig
from herre.grants.code_server.app import AuthorizationCodeServerGrant
from herre.grants.backend.app import BackendGrant
from herre.grants.backend.app import BackendGrant
import os
import logging
from koil import get_current_koil, Koil
import time

from koil.loop import koil

from fakts import Fakts, get_current_fakts, Config
from herre.grants.registry import GrantRegistry, get_current_grant_registry



logger = logging.getLogger(__name__)



class HerreError(Exception):
    pass


class Herre:

    def __init__(self,
        *args,
        register = True,
        config: HerreConfig = None,
        koil: Koil = None,
        fakts: Fakts = None,
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
        self.config = config 
        self.fakts = fakts or get_current_fakts()
        self.grant_registry = granty_registry or get_current_grant_registry()
        self.koil = koil or get_current_koil()
        self.grant = None

        if register:
            set_current_herre(self)

        super().__init__(*args, **kwargs)




    async def alogin(self, **kwargs):
        if not self.config:
            if not self.fakts.loaded:
                await self.fakts.aload()

            self.config = HerreConfig.from_fakts(fakts=self.fakts)
        
        self.grant = self.grant_registry.get_grant_for_type(self.config.authorization_grant_type)(self.config, fakts=self.fakts)
        return await self.grant.alogin(**kwargs)

    async def alogout(self):
        assert self.grant, "We have never logged in"
        return await self.grant.alogout()

    async def arefresh(self):
        assert self.grant, "We have never logged in"
        return await self.grant.arefresh()


    def login(self, **kwargs):
        return koil(self.alogin(), **kwargs)

    def logout(self, **kwargs):
        return koil(self.alogout(), **kwargs)
    
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