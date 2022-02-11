from abc import abstractmethod
from typing import Any, List
from herre.config import HerreConfig
from abc import ABC
import os
import logging
import aiohttp

logger = logging.getLogger(__name__)


class GrantException(Exception):
    pass


class RetryException(GrantException):
    pass


class BaseGrant(ABC):
    herre: Any
    is_user_grant: bool

    @abstractmethod
    async def afetch_token(self, herre, **kwargs):
        raise NotImplementedError("Impelment afetch_token")
