from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class GrantType(str, Enum):
    CLIENT_CREDENTIALS = "client-credentials"
    AUTHORIZATION_CODE = "authorization-code"


class App(BaseModel):
    clientID: Optional[str]
    name: Optional[str]


class User(BaseModel):
    sub: str  # This is not optional as openid spec demands it
    username: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class Token(BaseModel):
    access_token: str
    scope: Optional[List[str]]
    refresh_token: Optional[str]
    expires_in: Optional[int]
    expires_at: Optional[int]
    token_type: Optional[str]
