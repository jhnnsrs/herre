from abc import abstractmethod

from pydantic import BaseModel, Field
from herre.types import GrantType, Token
from typing import Any, List
from abc import ABC
import logging

logger = logging.getLogger(__name__)


class BaseGrant(BaseModel):
    @abstractmethod
    async def afetch_token(self, herre, **kwargs) -> Token:
        raise NotImplementedError("Implement afetch_token")

    class Config:
        underscore_attrs_are_private = True
