


from abc import abstractmethod
from herre.grants.models import User

from pydantic.main import prepare_config
from herre.console.context import get_current_console
from herre.config.herre import HerreConfig
from abc import ABC
import os 
import asyncio
import requests
import logging
import aiohttp


logger = logging.getLogger(__name__)

class BaseGrant(ABC):
    refreshable = False

    def __init__(self, config: HerreConfig, token_url="o/token/", authorize_url="o/authorize/") -> None:
        self.config = config
        if not config.secure: logger.warn("Using Insecure Oauth2 Protocol.. Please only for local and debug deployments")
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
        # State changed through Class
        self.can_refresh = self.refreshable


    @abstractmethod
    def fetchToken(self):
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


    def login(self, **kwargs):
        """IS SYNC!!!!
        """
        with get_current_console().status("[bold green] Authenticating"):
            self.fetchToken()
            assert "access_token" in self.token, "Returned token does not have an access_token"
            if "refresh_token" in self.token:
                self.can_refresh = True

        try:
            self._user = User(**requests.get(self.userinfo_url, headers={"Authorization": f"Bearer {self.access_token}"}).json())
        except:
            self._user = None


    async def refresh(self, **kwargs):
        assert "refresh_token" in self.token, "Token had not refresh-token attached"
        async with aiohttp.ClientSession() as session:
            async with session.post(self.refresh_url, data={"grant_type": "refresh_token", "refresh_token": self.token["refresh_token"], "client_id": self.config.client_id, "client_secret": self.config.client_secret}) as resp:
                self.token =  await resp.json()
                assert "access_token" in self.token, "Returned refreshed token does not have an access_token"
                if "refresh_token" in self.token:
                    self.can_refresh = True

