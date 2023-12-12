from typing import Dict, Type, Optional, Callable

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

    def register_grant(self, type: GrantType, grant: GrantBuilder) -> None:
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
        self.registered_grants[type] = grant

    def get_grant_for_type(self, type: GrantType) -> GrantBuilder:
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
        return self.registered_grants[type]

    class Config:
        """Pydantic config"""

        json_encoders = {type: lambda x: x.__name__}
        underscore_attrs_are_private = True


def register_grant(type: GrantType) -> Callable[[Type[BaseGrant]], Type[BaseGrant]]:
    """Decorator to register a grant

    This decorator registers a grant in the default grant registry.
    It can be used to register grants in the default grant registry.
    It is used by the fakts grant to build the correct grant from the fakts.

    """

    def real_decorator(grant: Type[BaseGrant]) -> Type[BaseGrant]:
        """The real decorator"""

        get_default_grant_registry().register_grant(type, grant)
        return grant

    return real_decorator


GRANT_REGISTRY: Optional[GrantRegistry] = None


def get_default_grant_registry() -> GrantRegistry:
    """Gets the default grant registry.

    If the default grant registry is not initialized, it will be initialized
    with the default grants.

    """

    global GRANT_REGISTRY
    if not GRANT_REGISTRY:
        GRANT_REGISTRY = GrantRegistry()
        from herre.grants.oauth2.client_credentials import ClientCredentialsGrant
        from herre.grants.oauth2.authorization_code_server import (
            AuthorizationCodeServerGrant,
        )

        GRANT_REGISTRY.register_grant(
            GrantType.AUTHORIZATION_CODE, AuthorizationCodeServerGrant
        )
        GRANT_REGISTRY.register_grant(
            GrantType.CLIENT_CREDENTIALS, ClientCredentialsGrant
        )

    return GRANT_REGISTRY
