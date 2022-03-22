from typing import Dict, Type

from pydantic import BaseModel, Field
from herre.grants.base import BaseGrant
from herre.types import GrantType
import logging


logger = logging.getLogger(__name__)


class GrantRegistry(BaseModel):
    _registered_grants: Dict[GrantType, Type[BaseGrant]] = None

    def register_grant(self, type: GrantType, grant: Type[BaseGrant]):
        if not self._registered_grants:
            self._registered_grants = {}
        assert hasattr(
            grant, "afetch_token"
        ), f"Grant {grant}must implement afetchtoken"
        self._registered_grants[type] = grant

    def get_grant_for_type(self, type):
        return self._registered_grants[type]

    class Config:
        json_encoders = {type: lambda x: x.__name__}
        underscore_attrs_are_private = True


def register_grant(type: GrantType):
    def real_decorator(grant):
        get_default_grant_registry().register_grant(type, grant)
        return grant

    return real_decorator


GRANT_REGISTRY = None


def get_default_grant_registry():
    global GRANT_REGISTRY
    if not GRANT_REGISTRY:
        GRANT_REGISTRY = GrantRegistry()
        from herre.grants.backend.app import BackendGrant
        from herre.grants.code_server.app import AuthorizationCodeServerGrant

        GRANT_REGISTRY.register_grant(
            GrantType.AUTHORIZATION_CODE, AuthorizationCodeServerGrant
        )
        GRANT_REGISTRY.register_grant(GrantType.CLIENT_CREDENTIALS, BackendGrant)

    return GRANT_REGISTRY
