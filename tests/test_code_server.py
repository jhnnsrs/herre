
from herre import Herre
from herre.grants.oauth2.authorization_code_server import AuthorizationCodeServerGrant
from herre.grants.oauth2.session import OAuth2Session
from .utils import fake_token_generator
import pytest

async def redirect_result(*args, **kwargs):
    return "path"


@pytest.mark.asyncio
async def test_code_server_mock_sync(monkeypatch):

    state = "soinsoisnosine"
    monkeypatch.setattr(
        OAuth2Session, "authorization_url", lambda self, t: ("xxxx", state)
    )
    monkeypatch.setattr(OAuth2Session, "fetch_token", fake_token_generator)

    x = Herre(
        grant=AuthorizationCodeServerGrant(
            client_id="UGqhHa2OS8NmTRjkVg8WKOWczYqkDVuK61yCueuO",
            client_secret="3oosB6FoC2iGASI8tkN16S8mPtlIvhqetvG5EOOJcLkn3txggTRxdp35G23CkNmvEY6fQXIXHaSzTa9Jb5Rk1hxWx0Fey0iUeOv2ZN568Z9z14kUbUbm4QQ1nacUW1gD",
            redirect_waiter=redirect_result,
            base_url="http://localhost:8000/o",
        )
    )

    async with x:
        await x.aget_token()
