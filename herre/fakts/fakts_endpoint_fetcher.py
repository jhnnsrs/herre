from pydantic import BaseModel, Field
import ssl
import certifi
import aiohttp
from herre.fetcher.types import Token
import logging
from herre.fetcher.errors import UserFetchingError
from fakts import Fakts
from typing import Type

logger = logging.getLogger(__name__)


class FaktsUserFetcher(BaseModel):
    """The endpoint to fetch the user from"""

    userModel: Type[BaseModel] = Field(
        description="The model to use for the user",
    )
    ssl_context: ssl.SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where()),
        exclude=True,
    )
    fakts: Fakts
    fakts_key: str

    """ An ssl context to use for the connection to the endpoint"""

    async def afetch_user(self, token: Token) -> BaseModel:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
            headers={"Authorization": f"Bearer {token.access_token}"},
        ) as session:
            async with session.get(
                await self.fakts.aget(self.fakts_key),
            ) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                        return self.userModel(**data)
                    except Exception as e:
                        logger.error(f"Malformed answer: {data}", exc_info=True)
                        raise UserFetchingError("Malformed Answer") from e

                else:
                    raise UserFetchingError("Error! Coud not retrieve on the endpoint")

    class Config:
        arbitrary_types_allowed = True
