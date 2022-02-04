from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class GrantType(str, Enum):
    IMPLICIT = "IMPLICIT"
    PASSWORD = "PASSWORD"
    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"
    AUTHORIZATION_CODE_SERVER = "AUTHORIZATION_CODE_SERVER"


class HerreConfig(BaseModel):
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
