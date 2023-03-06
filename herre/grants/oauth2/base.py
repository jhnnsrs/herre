from herre.grants.base import BaseGrant
from pydantic import SecretStr, Field
from typing import List
import ssl
import certifi
from ssl import SSLContext


class BaseOauth2Grant(BaseGrant):
    base_url: str
    client_id: SecretStr = SecretStr("")
    client_secret: SecretStr = SecretStr("")
    scopes: List[str] = Field(default_factory=lambda: list(["introspection"]))
    authorize_path: str = "authorize"
    refresh_path: str = "token"
    token_path: str = "token"
    scope_delimiter: str = " "
    allow_insecure: bool = False
    append_trailing_slash: bool = True

    ssl_context: SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where())
    )
