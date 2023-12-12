from herre import Herre
from herre.grants.static import StaticGrant, Token
import pytest

@pytest.mark.asyncio
async def test_mock_async():

    client = Herre(grant=StaticGrant(token=Token(access_token="hallo")))
    async with client:
        token = await client.aget_token()
        assert token, "No token retrieved"


def test_mock_sync():

    client = Herre(grant=StaticGrant(token=Token(access_token="hallo")))
    with client:
        token = client.get_token()
        assert token, "No token retrieved"
