from herre.types import GrantType, Token
from typing import List, Optional, Protocol, runtime_checkable, Type
from pydantic import BaseModel


@runtime_checkable
class UserFetcher(Protocol):
    userModel: Type[BaseModel]

    async def afetch_user(self, token: Token) -> BaseModel:
        ...
