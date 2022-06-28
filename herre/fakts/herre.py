from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, SecretStr

from fakts.fakt.base import Fakt
from fakts.fakts import get_current_fakts
from herre.errors import ConfigurationException
from herre.fakts.registry import GrantRegistry, get_default_grant_registry
from herre.herre import Herre
from herre.types import GrantType


class HerreFakt(Fakt):
    base_url: str
    name: str
    client_id: SecretStr
    client_secret: SecretStr
    grant_type: GrantType
    grant_kwargs: Dict[str, Any] = {}
    scopes: List[str]
    redirect_uri: Optional[str]
    jupyter_sync: bool = False
    username: Optional[str]
    password: Optional[str]
    timeout: int = 500
    no_temp: bool = False
    token_file: Optional[str] = "token.temp"


class FaktsHerre(Herre):
    grant_registry: GrantRegistry = Field(default_factory=get_default_grant_registry)
    base_url: Optional[str]
    name: Optional[str]
    fakts_group: str = "herre"

    _configured = False
    _old_fakt: Dict[str, Any] = {}

    def configure(self, fakt: HerreFakt) -> None:
        self.name = fakt.name
        self.token_file = f"{fakt.name}.token.temp"
        self.base_url = fakt.base_url
        self.client_id = fakt.client_id
        self.client_secret = fakt.client_secret

        self.grant = self.grant or self.grant_registry.get_grant_for_type(
            fakt.grant_type
        )(**fakt.grant_kwargs)

    async def alogin(self, force_refresh=False, retry=0):
        fakts = get_current_fakts()
        print(self._old_fakt)

        if fakts.has_changed(self._old_fakt, self.fakts_group):
            print("FAKTS HAVE CHANGED")
            self._old_fakt = await fakts.aget(self.fakts_group)
            self.configure(HerreFakt(**self._old_fakt))
        try:
            return await super().alogin(force_refresh, retry)
        except ConfigurationException:
            await fakts.arefresh()
            await self.alogin(force_refresh, retry + 1)

    async def __aenter__(self, **kwargs):
        return await super().__aenter__(**kwargs)
