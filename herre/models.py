""" Basic types for the herre library

This module contains the basic types for the herre library.

"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time


class TokenRequest(BaseModel):
    """A token request

    A token request is initiated by the client and contains all the information
    needed to request a token from the server.

    Grants can inspect the request and decide whether to handle it or not.
    Additionailly, they can modify the request before it is sent to the next grant.

    """

    is_refresh: bool = False
    """Whether this is a refresh request"""
    context: Dict[str, Any]
    """The context of the request"""


class Token(BaseModel):
    """A Token

    A token object contains all the information about a token.
    It mimics the oauthlib.oauth2.rfc6749.tokens.OAuthToken class.
    However, you can use it with any grant, not just oauth2 grants.
    As access_token is the only required field, you can use it as a simple
    bearer token.

    """

    access_token: str
    scope: Optional[List[str]] = Field(default_factory=list)
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    expires_at: Optional[int] = None
    token_type: Optional[str] = None

    def is_expired(self) -> bool:
        """Checks if the token is expired"""
        if self.expires_at:
            return self.expires_at < int(time.time())
        return False
