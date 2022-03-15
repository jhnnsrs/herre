from abc import abstractmethod
from herre.grants.base import BaseGrant
from herre.types import Token, User
from typing import Any, List
from abc import ABC
import logging

logger = logging.getLogger(__name__)


class UserGrant(BaseGrant):
    herre: Any

    @abstractmethod
    async def afetch_token(self, herre, **kwargs) -> Token:
        raise NotImplementedError("Implement afetch_token")

    @abstractmethod
    async def afetch_user(self, herre, token: Token) -> User:
        raise NotImplementedError("Implement afetch_token")
