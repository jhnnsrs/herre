from abc import ABC, abstractmethod
import aiohttp
from herre.herre import Herre


class RefreshableGrant:
    type = None

    @abstractmethod
    async def afetch_token(self, herre: Herre):
        raise NotImplementedError()

    async def arefresh(self, herre: Herre):
        assert "refresh_token" in self.token, "Token had not refresh-token attached"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                herre.refresh_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.token["refresh_token"],
                    "client_id": herre.client_id,
                    "client_secret": herre.client_secret,
                },
            ) as resp:
                self.token = await resp.json()
                assert (
                    "access_token" in self.token
                ), "Returned refreshed token does not have an access_token"
                if "refresh_token" in self.token:
                    self.can_refresh = True

    
