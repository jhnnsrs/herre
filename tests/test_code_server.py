import webbrowser
from herre import Herre, utils
from herre.grants.backend.app import BackendGrant
from herre.grants.code_server.app import AuthorizationCodeServerGrant
from herre.grants.test.app import MockGrant
from herre.grants.session import OAuth2Session
from herre.types import User


async def fake_token_generator(*args, **kwargs):
    return {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
    }


async def fake_user_generator(*args, **kwargs):
    return User(sub="fake_user")


async def redirect_result(*args, **kwargs):
    return "path"


async def test_code_server_mock_sync(monkeypatch):

    state = "soinsoisnosine"
    monkeypatch.setattr(
        OAuth2Session, "authorization_url", lambda self, t: ("xxxx", state)
    )
    monkeypatch.setattr(
        AuthorizationCodeServerGrant, "get_path_from_redirect", redirect_result
    )
    monkeypatch.setattr(OAuth2Session, "fetch_token", fake_token_generator)
    monkeypatch.setattr(
        AuthorizationCodeServerGrant, "afetch_user", fake_user_generator
    )

    x = Herre(
        base_url="http://localhost:8000/o",
        grant=AuthorizationCodeServerGrant(),
        client_id="UGqhHa2OS8NmTRjkVg8WKOWczYqkDVuK61yCueuO",
        client_secret="3oosB6FoC2iGASI8tkN16S8mPtlIvhqetvG5EOOJcLkn3txggTRxdp35G23CkNmvEY6fQXIXHaSzTa9Jb5Rk1hxWx0Fey0iUeOv2ZN568Z9z14kUbUbm4QQ1nacUW1gD",
        no_temp=True,
    )

    async with x:
        await x.aget_token()
