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
    client_id: SecretStr
    client_secret: SecretStr
    authorization_grant_type: GrantType
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
    grant_registry: GrantRegistry = Field(default_factory=get_default_grant_registry)

    def configure(self, config: HerreConfig, fakts: Fakts) -> None:
        self.token_file = f"{fakts.subapp}.token.temp"
        self.base_url = config.base_url
        self.client_id = self.client_id or config.client_id
        self.client_secret = self.client_secret or config.client_secret
        self.token_file = self.token_file or config.token_file

        self.grant = self.grant or self.grant_registry.get_grant_for_type(
            config.authorization_grant_type
        )(**config.grant_kwargs)

    async def __aenter__(self, **kwargs):
        fakts = current_fakts.get()
        config = await HerreConfig.from_fakts(fakts)
        self.configure(config, fakts)

        return await super().__aenter__(**kwargs)
