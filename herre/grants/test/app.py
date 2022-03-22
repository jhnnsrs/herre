from herre.grants.base import BaseGrant
from herre.types import Token, User
from herre.herre import Herre


class MockGrant(BaseGrant):
    async def afetch_token(self, herre: Herre) -> Token:
        return Token(access_token="mock_token", refresh_token="mock_refresh_token")

    async def afetch_user(self, herre: Herre, token: Token):
        return User(sub="1")
