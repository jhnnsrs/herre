from typing import List, Optional
from pydantic import BaseModel


class App(BaseModel):
    clientID: Optional[str]
    name: Optional[str]


class User(BaseModel):
    username: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class HerreState(BaseModel):
    user: Optional[User]
    scopes: List[str]
    client_id: str
    access_token: str
    refresh_token: Optional[str]
