from pydantic import BaseModel, Field
import ssl
import certifi
import aiohttp
from .models import Token
import logging
from .errors import UserFetchingError
from typing import Type

logger = logging.getLogger(__name__)


class UserinfoUserFetcher(BaseModel):
    """A user fetcher that fetches the user from an userinfo endpoint.

    This fetcher uses the userinfo endpoint to fetch the user. It uses the access token to
    authenticate itself to the userinfo endpoint.

    You can specify the model to use for the user. This model will be used to parse the answer
    from the userinfo endpoint. The model should be a pydantic model.


    """

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
        """Fetches the user from the userinfo endpoint.

        Parameters:
        ___________
        token: Token
            The token to use to authenticate to the userinfo endpoint.

        Returns:
        ________
        BaseModel
            The user as a pydantic model (will be userModel)

        """
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
                    raise UserFetchingError(
                        "Error! Coud not retrieve on the endpoint. Maybe your token is invalid? Or you forgot to add the `openid` scope?"
                    )
