from pydantic import BaseModel, Field
import ssl
import certifi
import aiohttp
from .types import Token
import logging
from .errors import UserFetchingError
from typing import Type

logger = logging.getLogger(__name__)


class UserinfoUserFetcher(BaseModel):
    userModel: Type[BaseModel] = Field(
        description="The model to use for the user",
    )
    """ The model to use for the user"""
    userinfo_endpoint: str = Field(
        default="https://localhost:8000/userinfo",
        description="The endpoint to fetch the user from",
    )
    """ The endpoint to fetch the user from"""
    ssl_context: ssl.SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where()),
        exclude=True,
    )
    """ An ssl context to use for the connection to the endpoint"""

    async def afetch_user(self, token: Token) -> BaseModel:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=self.ssl_context),
            headers={"Authorization": f"Bearer {token.access_token}"},
        ) as session:
            async with session.get(
                f"{self.userinfo_endpoint}",
            ) as resp:
                if resp.status == 200:
                    try:
                        data = await resp.json()
                        return self.userModel(**data)
                    except Exception as e:
                        logger.error(f"Malformed answer: {data}")
                        raise UserFetchingError("Malformed Answer") from e

                else:
                    raise UserFetchingError("Error! Coud not retrieve on the endpoint")
