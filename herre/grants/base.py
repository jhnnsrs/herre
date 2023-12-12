from abc import abstractmethod

from pydantic import BaseModel
from herre.models import Token, TokenRequest
from typing import Protocol, runtime_checkable
import logging

logger = logging.getLogger(__name__)


@runtime_checkable
class BaseGrantProtocol(Protocol):
    """The base grant protocol

    This protocol is implemented by all grants.
    It can be used to type hint a grant.

    """

    async def afetch_token(self, request: TokenRequest) -> Token:
        """Fetches a token

        This function will fetch a token from the grant.
        This function is async, and should be awaited

        Parameters
        ----------
        request : TokenRequest
            The token request to use

        Returns
        -------
        Token
            The token
        """
        ...


class BaseGrant(BaseModel):
    """The base grant class

    This class is the base class for all grants.
    It is a pydantic model, and can be used as such.
    It also implements the BaseGrantProtocol, which can be used to type hint
    a grant.

    """

    @abstractmethod
    async def afetch_token(self, request: TokenRequest) -> Token:
        """Fetches a token

        This function will fetch a token from the grant.
        This function is async, and should be awaited

        Parameters
        ----------
        request : TokenRequest
            The token request to use

        Returns
        -------
        Token
            The token
        """
        raise NotImplementedError("Implement afetch_token")

    class Config:
        """Config for the base grant"""

        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
        extras = "forbid"
