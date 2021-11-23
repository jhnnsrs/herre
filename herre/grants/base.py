


from abc import abstractmethod

from pydantic.main import prepare_config
from herre.console.context import get_current_console
from herre.config import HerreConfig
from abc import ABC
import os 
import logging
import aiohttp
import shelve

from fakts import Fakts, get_current_fakts, Config

logger = logging.getLogger(__name__)


class GrantException(Exception):
    pass

class RetryException(GrantException):
    pass




class BaseGrant(ABC):
    refreshable = False
    type = None

    def __init__(self, herre_config: HerreConfig,  token_url="o/token/", authorize_url="o/authorize/", token_file: str = "token.temp", save_token = True, max_retries = 3, facts: Fakts = None, **kwargs) -> None:
        self.facts = facts or get_current_fakts()
        self.config = herre_config
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0" if self.config.secure else "1"


        self.base_url = f'{"https" if self.config.secure else "http"}://{self.config.host}:{self.config.port}{self.config.subpath}/'
        self.auth_url = self.base_url + authorize_url
        self.token_url = self.base_url + token_url
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


    async def arefresh(self, **kwargs):
        if not self.refreshable: return None
        assert "refresh_token" in self.token, "Token had not refresh-token attached"
        async with aiohttp.ClientSession() as session:
            async with session.post(self.refresh_url, data={"grant_type": "refresh_token", "refresh_token": self.token["refresh_token"], "client_id": self.config.client_id, "client_secret": self.config.client_secret}) as resp:
                self.token =  await resp.json()
                assert "access_token" in self.token, "Returned refreshed token does not have an access_token"
                if "refresh_token" in self.token:
                    self.can_refresh = True

