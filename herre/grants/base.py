from abc import abstractmethod
from ssl import SSLContext
import ssl
import certifi

from pydantic import BaseModel, Field
from herre.types import GrantType, Token
from typing import Any, List
from abc import ABC
import logging

logger = logging.getLogger(__name__)


class BaseGrant(BaseModel):
    ssl_context: SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where())
    )

    @abstractmethod
    async def afetch_token(self, herre, **kwargs) -> Token:
        raise NotImplementedError("Implement afetch_token")

    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
