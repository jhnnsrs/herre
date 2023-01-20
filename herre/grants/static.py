from herre.grants.base import BaseGrant
from herre.types import Token


class StaticGrant(BaseGrant):
    token: Token

    async def afetch_token(self, force_refresh: bool=False) -> Token:
        return self.token
