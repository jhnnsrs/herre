from typing import Dict, Callable

from pydantic import BaseModel, Field
from herre.grants.base import BaseGrant
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class GrantType(str, Enum):
    """The grant type"""

    CLIENT_CREDENTIALS = "client-credentials"
    """The client credentials grant"""
    AUTHORIZATION_CODE = "authorization-code"
    """The authorization code grant"""


GrantBuilder = Callable[..., BaseGrant]
#


class GrantRegistry(BaseModel):
    """A registry for grants.

    This registry is used to register grants. It is used by the fakts
    grant to build the correct grant from the fakts.


    """

    registered_grants: Dict[GrantType, GrantBuilder] = Field(default_factory=dict)

    def register_grant(self, grant_type: GrantType, grant: GrantBuilder) -> None:
        """Registers a grant.

        Parameters:
        ___________
        type: GrantType
            The type of the grant to register
        grant: Type[BaseGrant]
            The grant to register

        """
        if not self.registered_grants:
            self.registered_grants = {}
        self.registered_grants[grant_type] = grant

    def get_grant_for_type(self, grant_type: GrantType) -> GrantBuilder:
        """Gets the grant for a type.

        Parameters:
        ___________
        type: GrantType
            The type of the grant to get

        Returns:
        ________
        Type[BaseGrant]
            The grant for the type

        """
        return self.registered_grants[grant_type]

    class Config:
        """Pydantic config"""

        json_encoders = {type: lambda x: x.__name__}
        underscore_attrs_are_private = True
