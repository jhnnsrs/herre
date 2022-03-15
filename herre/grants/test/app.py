from herre.grants.base import BaseGrant
from herre.types import Token, User
from herre.herre import Herre


class MockGrant(BaseGrant):
    refreshable = True
    is_user_grant = False

    def __init__(
        self,
        redirect_timeout=40,
    ) -> None:
        self.redirect_timeout = redirect_timeout

    async def afetch_token(self, herre: Herre) -> Token:
        return Token(access_token="mock_token", refresh_token="mock_refresh_token")

    async def afetch_user(self, herre: Herre, token: Token):
        return User(sub="1")
