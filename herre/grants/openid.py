from abc import ABC, abstractmethod
from herre.grants.errors import NoUserException
from herre.grants.utils import build_refresh_url
from herre.types import Token, User
import aiohttp
from herre.grants.base import BaseGrant
from herre.herre import Herre, build_userinfo_url


class OpenIdUser:
    async def afetch_user(self, herre: Herre, token: Token) -> User:
        async with aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {token.access_token}"}
        ) as session:
            async with session.get(build_userinfo_url(herre)) as resp:

                user_json = await resp.json()
                if "detail" in user_json:
                    raise NoUserException(user_json["detail"])

                return User(**user_json)
