from fakts.config.base import Config
from fakts.fakts import Fakts, current_fakts
from herre.herre import Herre
from herre.fakts.registry import (
    GrantRegistry,
    get_default_grant_registry,
)
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, SecretStr

from herre.types import GrantType


class HerreConfig(Config):
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

    class Config:
        group: str = "herre"


class FaktsHerre(Herre):
    fakts_group: str = "herre"
    grant_registry: GrantRegistry = Field(default_factory=get_default_grant_registry)
    base_url: Optional[str]
    name: Optional[str]

    _configured = False

    def configure(self, config: HerreConfig) -> None:
        self.name = config.name
        self.token_file = f"{config.name}.token.temp"
        self.base_url = config.base_url
        self.client_id = self.client_id or config.client_id
        self.client_secret = self.client_secret or config.client_secret
        self.token_file = self.token_file or config.token_file

        self.grant = self.grant or self.grant_registry.get_grant_for_type(
            config.grant_type
        )(**config.grant_kwargs)

    async def alogin(self, force_refresh=False, retry=0):
        if not self._configured:
            config = await HerreConfig.from_fakts(self.fakts_group)
            self.configure(config)

        return await super().alogin(force_refresh, retry)

    async def __aenter__(self, **kwargs):
        return await super().__aenter__(**kwargs)
