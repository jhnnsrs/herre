from abc import ABC, abstractmethod
from herre.grants.utils import build_refresh_url
from herre.types import Token
import aiohttp
from herre.grants.base import BaseGrant
from herre.herre import Herre


class Refreshable:
    type = None

    @abstractmethod
    async def afetch_token(self, herre: Herre):
        raise NotImplementedError()

    async def arefresh(self, herre: Herre, token: Token):
        assert token.refresh_token, "Token had not refresh-token attached"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                build_refresh_url(herre),
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.token["refresh_token"],
                    "client_id": herre.client_id.get_secret_value(),
                    "client_secret": herre.client_secret.get_secret_value(),
                },
            ) as resp:
                self.token = await resp.json()
                assert (
                    "access_token" in self.token
                ), "Returned refreshed token does not have an access_token"
                if "refresh_token" in self.token:
                    self.can_refresh = True
