from herre.grants.base import BaseGrant
from pydantic import SecretStr, Field
from typing import List
import ssl
import certifi
from ssl import SSLContext


class BaseOauth2Grant(BaseGrant):
    """A base class for oauth2 grants."""

    base_url: str
    """The base url to use for the grant"""

    client_id: SecretStr = SecretStr("")
    """The client id to use for the grant"""
    client_secret: SecretStr = SecretStr("")  #
    """The client secret to use for the grant"""
    scopes: List[str] = Field(default_factory=lambda: list(["openid"]))
    """The scopes to use for the grant"""
    authorize_path: str = "authorize"
    """The authorize path to use for the grant (relative to the base url)"""
    refresh_path: str = "token"
    """The refresh path to use for the grant (relative to the base url)"""
    token_path: str = "token"
    """The token path to use for the grant (relative to the base url)"""
    scope_delimiter: str = " "
    """The scope delimiter to use for the grant default is a space"""
    allow_insecure: bool = False
    """Whether to allow insecure connections"""
    append_trailing_slash: bool = True
    """Whether to append a trailing slash to the base url"""

    ssl_context: SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where())
    )
