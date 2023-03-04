from abc import abstractmethod

from pydantic import BaseModel
from herre.types import Token
import logging

logger = logging.getLogger(__name__)


class BaseGrant(BaseModel):

    @abstractmethod
    async def afetch_token(self, force_refresh: bool =False) -> Token:
        raise NotImplementedError("Implement afetch_token")

    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
