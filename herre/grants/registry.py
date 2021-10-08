from typing import Dict
from .base import BaseGrant
from herre.config import GrantType


class GrantRegistry:

    def __init__(self) -> None:
        self.registeredGrants: Dict[str, BaseGrant] = {}

    def register_grant(self, type: GrantType,  grant: BaseGrant):
        self.registeredGrants[type] = grant

    def get_grant_for_type(self,type):
        return self.registeredGrants[type]

    
def register_grant(type: GrantType):
    print("Registering Grant")

    def rea_decorator(grant):
        assert issubclass(grant, BaseGrant), "Grant must subclass BaseGrant"
        get_current_grant_registry().register_grant(type, grant)
        return grant

    return rea_decorator



GRANT_REGISTRY = None


def get_current_grant_registry(with_defaults=True):
    global GRANT_REGISTRY
    if not GRANT_REGISTRY:
        GRANT_REGISTRY = GrantRegistry()
        if with_defaults:
            import herre.grants.backend.app 
            import herre.grants.code_server.app


    return GRANT_REGISTRY