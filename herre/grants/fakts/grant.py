from typing import Any, Dict, List, Optional, Type, runtime_checkable, Protocol
from fakts import get_current_fakts
from pydantic import BaseModel, Field, SecretStr
from herre.grants.base import BaseGrant
from .registry import GrantRegistry, get_default_grant_registry
from herre.types import GrantType
from herre.grants.oauth2.base import BaseOauth2Grant
from oauthlib.oauth2.rfc6749.errors import InvalidClientError


class HerreFakt(BaseModel):
    base_url: str
    name: str
    client_id: SecretStr
    client_secret: SecretStr
    grant_type: GrantType
    grant_kwargs: Dict[str, Any] = {}
    scopes: List[str]
    redirect_uri: Optional[str]
    username: Optional[str]
    password: Optional[str]
    timeout: int = 500
    no_temp: bool = False

@runtime_checkable
class BaseGrantFactory(Protocol):

    def __call__(self, **kwds: Any) -> BaseGrant:
        pass


class FaktsGrant(BaseOauth2Grant):
    base_url: Optional[str] = None
    grant_class: Optional[BaseGrantFactory]
    grant_registry: GrantRegistry = Field(default_factory=get_default_grant_registry)
    fakts_group: str = "lok"
    allow_reconfiguration_on_invalid_client: bool = True

    _configured = False
    _activegrant: Optional[BaseGrant] = None
    _old_fakt: Dict[str, Any] = {}

    def configure(self, fakt: HerreFakt) -> None:
        grant_class = self.grant_class or self.grant_registry.get_grant_for_type(
            fakt.grant_type
        )

        self._activegrant = grant_class(**fakt.dict())

    async def afetch_token(self, force_refresh=False):
        fakts = get_current_fakts()

        if fakts.has_changed(self._old_fakt, self.fakts_group):
            self._old_fakt = await fakts.aget(self.fakts_group)
            self.configure(HerreFakt(**self._old_fakt))

        try:
            return await self._activegrant.afetch_token(force_refresh=force_refresh)
        except InvalidClientError as e:
            if self.allow_reconfiguration_on_invalid_client:
                self._old_fakt = await fakts.aget(self.fakts_group, force_refresh=True)
                self.configure(HerreFakt(**self._old_fakt))
                return await self._activegrant.afetch_token(force_refresh=True)
            else:
                raise e

    async def __aenter__(self, **kwargs):
        return await super().__aenter__(**kwargs)
