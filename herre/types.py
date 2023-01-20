from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
import time

class GrantType(str, Enum):
    CLIENT_CREDENTIALS = "client-credentials"
    AUTHORIZATION_CODE = "authorization-code"


class Token(BaseModel):
    access_token: str
    scope: Optional[List[str]]
    refresh_token: Optional[str]
    expires_in: Optional[int]
    expires_at: Optional[int]
    token_type: Optional[str]

    def is_expired(self) -> bool:
        if self.expires_at:
            return self.expires_at < int(time.time())
        return False
