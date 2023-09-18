from herre.grants.base import BaseGrant
from herre.types import Token, TokenRequest


class StaticGrant(BaseGrant):
    token: Token

    async def afetch_token(self, request: TokenRequest) -> Token:
        return self.token
