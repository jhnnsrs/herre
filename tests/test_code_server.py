from herre import Herre
from herre.grants.oauth2.authorization_code import AuthorizationCodeGrant
from herre.grants.oauth2.redirecters import MockRedirecter
import pytest


@pytest.mark.asyncio
async def test_code_server_mock_sync(valid_token_response):
    state = "soinsoisnosine"

    x = Herre(
        grant=AuthorizationCodeGrant(
            client_id="UGqhHa2OS8NmTRjkVg8WKOWczYqkDVuK61yCueuO",
            client_secret="3oosB6FoC2iGASI8tkN16S8mPtlIvhqetvG5EOOJcLkn3txggTRxdp35G23CkNmvEY6fQXIXHaSzTa9Jb5Rk1hxWx0Fey0iUeOv2ZN568Z9z14kUbUbm4QQ1nacUW1gD",
            redirecter=MockRedirecter(code="mock_code"),
            base_url="http://localhost:8000/o",
        )
    )

    async with x:
        await x.aget_token()
