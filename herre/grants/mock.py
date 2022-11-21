from herre.grants.base import BaseGrant
from herre.types import Token


class MockGrant(BaseGrant):
    async def afetch_token(self, force_refresh=False) -> Token:
        return Token(access_token="mock_token", refresh_token="mock_refresh_token")
