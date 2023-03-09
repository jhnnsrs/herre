from herre.grants.qt.login_screen import (
    QtLoginScreen,
    Token,
    User,
    MalformedAnswerException,
    FetchingUserException,
)
from typing import Optional
from fakts import get_current_fakts, Fakts
import logging
import aiohttp
from pydantic import Field

logger = logging.getLogger(__name__)


class FaktsQtLoginScreen(QtLoginScreen):
    userinfo_endpoint: Optional[str]
    fakts_group: str = "lok"
    fakts: Optional[Fakts] = None
    fetch_timeout: int = Field(default=3, description="Timeout for fetching the user")

    _userinfo_endpoint = None

    """ An ssl context to use for the connection to the endpoint"""

    async def aget_userinfo_endpoint(self) -> str:
        fakts = get_current_fakts()
        unserialized = await fakts.aget(self.fakts_group)
        self.userinfo_endpoint = unserialized["base_url"] + "/me/"
        return unserialized["base_url"] + "/me/"

    async def afetch_user(self, token: Token) -> User:
        if not self._userinfo_endpoint:
            self._userinfo_endpoint = await self.aget_userinfo_endpoint()

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
            headers={"Authorization": f"Bearer {token.access_token}"},
        ) as session:
            async with session.get(
                f"{self.userinfo_endpoint}",
                timeout=self.fetch_timeout,
            ) as resp:
                data = await resp.json()

                if resp.status == 200:
                    data = await resp.json()
                    if "username" not in data:
                        logger.error(f"Malformed answer: {data}")
                        raise MalformedAnswerException("Malformed Answer")

                    return User(**data)

                else:
                    raise FetchingUserException(
                        "Error! Coud not retrieve on the endpoint"
                    )
