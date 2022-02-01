from abc import abstractmethod
from typing import List
from herre.config import HerreConfig
from abc import ABC
import os
import logging
import aiohttp

logger = logging.getLogger(__name__)


class GrantException(Exception):
    pass


class RetryException(GrantException):
    pass


class DefaultGrant(ABC):
    refreshable = False
    type = None

    def __init__(
        self,
        base_url,
        client_id,
        client_secret,
        scopes=["introspection"],
        token_url="o/token/",
        authorize_url="o/authorize/",
        secure=False,
        max_retries=3,
        **kwargs,
    ) -> None:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0" if secure else "1"

        self.base_url = base_url
        self.auth_url = self.base_url + authorize_url
        self.token_url = self.base_url + token_url
        self.refresh_url = self.token_url
        self._userinfo = None

        self.scopes = scopes
        self.scope = " ".join(self.scopes)
        self.token = None
        self.max_retries = max_retries
        self.client_id = client_id
        self.client_secret = client_secret

        # State changed through Class
        self.can_refresh = self.refreshable

    @abstractmethod
    async def afetch_token(self, **kwargs):
        raise NotImplementedError()

    async def arefresh(self, **kwargs):
        if not self.refreshable:
            return None
        assert "refresh_token" in self.token, "Token had not refresh-token attached"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.refresh_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.token["refresh_token"],
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            ) as resp:
                self.token = await resp.json()
                assert (
                    "access_token" in self.token
                ), "Returned refreshed token does not have an access_token"
                if "refresh_token" in self.token:
                    self.can_refresh = True


class BaseGrant(ABC):
    client_id: str
    client_secret: str
    scopes: List[str]

    @abstractmethod
    async def afetch_token(self, **kwargs):
        raise NotImplementedError("Impelment afetch_token")
