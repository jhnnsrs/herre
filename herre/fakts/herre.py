from fakts.config.base import Config
from fakts.fakts import Fakts, current_fakts
from herre.herre import Herre
from herre.fakts.registry import GrantRegistry, get_current_grant_registry
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class GrantType(str, Enum):
    IMPLICIT = "IMPLICIT"
    PASSWORD = "PASSWORD"
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"
    AUTHORIZATION_CODE_SERVER = "AUTHORIZATION_CODE_SERVER"


class HerreConfig(Config):
    base_url: str
    client_id: str
    client_secret: str
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
    def __init__(
        self,
        *args,
        fakts: Fakts = None,
        grant_registry: GrantRegistry = None,
        fakts_key="herre",
        token_file=None,
        **kwargs,
    ) -> None:
        super().__init__(*args, token_file=token_file, **kwargs)
        self.fakts = fakts
        self.config = None
        self._fakts_key = fakts_key
        self._grant_registry = grant_registry

    def configure(self, config: HerreConfig, fakts: Fakts) -> None:
        self.token_file = f"{fakts.subapp}.token.temp"
        self.base_url = config.base_url
        self.client_id = self.client_id or config.client_id
        self.client_secret = self.client_secret or config.client_secret
        self.token_file = self.token_file or config.token_file

        self.grant = self.grant or self._grant_registry.get_grant_for_type(
            config.authorization_grant_type
        )(**config.grant_kwargs)

        self.configured = True
        self.config = config

    async def alogin(self, **kwargs):

        if not self.config:
            fakts = self.fakts or current_fakts.get()
            self._grant_registry = self._grant_registry or get_current_grant_registry()
            config = await HerreConfig.from_fakts(fakts)
            self.configure(config, fakts)

        return await super().alogin(**kwargs)
