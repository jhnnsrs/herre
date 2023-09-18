""" Basic types for the herre library

This module contains the basic types for the herre library.

"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import time


class GrantType(str, Enum):
    """The grant type"""

    CLIENT_CREDENTIALS = "client-credentials"
    AUTHORIZATION_CODE = "authorization-code"


class TokenRequest(BaseModel):
    is_refresh: bool = False
    context: Dict[str, Any]


class Token(BaseModel):
    """A token object"""

    access_token: str
    scope: Optional[List[str]]
    refresh_token: Optional[str]
    expires_in: Optional[int]
    expires_at: Optional[int]
    token_type: Optional[str]

    def is_expired(self) -> bool:
        """Checks if the token is expired"""
        if self.expires_at:
            return self.expires_at < int(time.time())
        return False
