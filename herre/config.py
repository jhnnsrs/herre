from enum import Enum
from typing import List, Optional

from fakts import Fakts, get_current_fakts, Config




class GrantType(str, Enum):
    IMPLICIT = "IMPLICIT"
    PASSWORD = "PASSWORD"
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"
    AUTHORIZATION_CODE_SERVER = "AUTHORIZATION_CODE_SERVER"

class HerreConfig(Config):
    subpath: str = ""
    secure: bool 
    host: str
    port: int
    client_id: str 
    client_secret: str
    authorization_grant_type: GrantType
    scopes: List[str]
    redirect_uri: Optional[str]
    jupyter_sync: bool = False
    username: Optional[str]
    password: Optional[str]
    timeout: int = 500

    class Config:
        group = "herre"