from herre.config.base import BaseConfig
from enum import Enum
from typing import List, Optional


class GrantType(str, Enum):
    IMPLICIT = "IMPLICIT"
    PASSWORD = "PASSWORD"
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    AUHORIZATION_CODE = "AUTHORIZATION_CODE"

class HerreConfig(BaseConfig):
    _group = "herre"

    secure: bool 
    host: str
    port: int 
    client_id: str 
    client_secret: str
    authorization_grant_type: GrantType
    scopes: List[str]
    redirect_uri: Optional[str]

    def __str__(self) -> str:
        return f"{'Secure' if self.secure else 'Insecure'} Connection to {self.host}:{self.port} on Grant {self.authorization_grant_type}"

    