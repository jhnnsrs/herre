


from abc import abstractmethod
from herre.grants.models import User

from pydantic.main import prepare_config
from herre.console.context import get_current_console
from herre.config import HerreConfig
from abc import ABC
import os 
import asyncio
import requests
import logging
import aiohttp
import shelve
from konfik import get_current_konfik, Konfik

logger = logging.getLogger(__name__)


class GrantException(Exception):
    pass

class RetryException(GrantException):
    pass




class BaseGrant(ABC):
    refreshable = False
    type = None

    def __init__(self, herre_config: HerreConfig,  token_url="o/token/", authorize_url="o/authorize/", token_file: str = "token.temp", save_token = True, max_retries = 3, konfik: Konfik = None, **kwargs) -> None:
        self.konfik = konfik or get_current_konfik()
        self.config = herre_config
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0" if self.config.secure else "1"


        self.base_url = f'{"https" if self.config.secure else "http"}://{self.config.host}:{self.config.port}/'
        self.auth_url = self.base_url + authorize_url
        self.token_url = self.base_url + token_url
        self.userinfo_url = self.base_url + "userinfo/"
        self.refresh_url = self.token_url
        self._userinfo = None
       
        self.scopes = self.config.scopes + ["introspection"]
        self.scope = " ".join(self.scopes)
        self.token = None
        self._user = None
        self.token_file = token_file
        self.save_token = save_token
        self.max_retries = max_retries

        # State changed through Class
        self.can_refresh = self.refreshable


    @abstractmethod
    async def afetch_token(self, **kwargs):
        raise NotImplementedError()

    @property
    def user(self) -> User:
        return self._user


    @property
    def logged_in(self):
        return self.token is not None

    @property
    def access_token(self):
        assert self.token is not None, "You need to login before you can use this function. Call Herre.login()"
        return self.token["access_token"]


    async def alogin(self, force_relogin=False, retry=0, **kwargs):
        """IS SYNC!!!!
        """
        if retry > self.max_retries: raise RetryException("Grant exceeded login retries")
        self.token = None
        if not force_relogin:
            try:
                with shelve.open(self.token_file) as cfg:
                    self.token = cfg['token']
            except KeyError:
                pass

        self.token = self.token or await self.fetch_token(**kwargs)
        assert self.token is not None, "We have received not Token back from our Grant"
        assert "access_token" in self.token, "Returned token does not have an access_token"


        if "refresh_token" in self.token:
            self.can_refresh = True

        
        try:
            async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {self.access_token}"}) as session:
                async with session.get(self.userinfo_url) as resp:
                    user_json = await resp.json()
                    self._user = User(**user_json)

                    if self.save_token:
                        with shelve.open(self.token_file) as cfg:
                            cfg['token'] = self.token

        except Exception as e:
            logger.exception(e)
            await self.alogin(force_relogin=True, **kwargs)
            

    async def alogout(self, force_relogin=False, **kwargs):
        """IS SYNC!!!!
        """
        try:
            with shelve.open(self.token_file) as cfg:
                cfg["token"] = None
        except KeyError:
            pass

        self.token = None
        self._user = None


    async def arefresh_token(self, **kwargs):
        assert "refresh_token" in self.token, "Token had not refresh-token attached"
        async with aiohttp.ClientSession() as session:
            async with session.post(self.refresh_url, data={"grant_type": "refresh_token", "refresh_token": self.token["refresh_token"], "client_id": self.config.client_id, "client_secret": self.config.client_secret}) as resp:
                self.token =  await resp.json()
                assert "access_token" in self.token, "Returned refreshed token does not have an access_token"
                if "refresh_token" in self.token:
                    self.can_refresh = True

