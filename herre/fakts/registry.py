from typing import Dict, Type
from herre.grants.base import BaseGrant
from herre.types import GrantType
import logging


logger = logging.getLogger(__name__)


class GrantRegistry:
    def __init__(self, register_defaults=True) -> None:
        self.registeredGrants: Dict[str, BaseGrant] = {}
        if register_defaults:
            self.register_defaults()

    def register_defaults(self):
        from herre.grants.backend.app import BackendGrant
        from herre.grants.code_server.app import AuthorizationCodeServerGrant

        self.register_grant(GrantType.AUTHORIZATION_CODE, AuthorizationCodeServerGrant)
        self.register_grant(GrantType.CLIENT_CREDENTIALS, BackendGrant)

    def register_grant(self, type: GrantType, grant: Type[BaseGrant]):
        self.registeredGrants[type] = grant

    def get_grant_for_type(self, type):
        return self.registeredGrants[type]


def register_grant(type: GrantType):
    def real_decorator(grant):
        assert hasattr(
            grant, "afetchtoken"
        ), "A grant must specify a afetchtoken method"
        logger.info(f"Registering Grant {grant} for {type}")
        get_default_grant_registry().register_grant(type, grant)
        return grant

    return real_decorator


GRANT_REGISTRY = None


def get_default_grant_registry():
    global GRANT_REGISTRY
    if not GRANT_REGISTRY:
        GRANT_REGISTRY = GrantRegistry()

    return GRANT_REGISTRY
