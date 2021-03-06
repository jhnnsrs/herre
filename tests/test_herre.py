from herre import Herre
from herre.grants.test.app import MockGrant


async def test_mock_async():

    client = Herre(grant=MockGrant(), no_temp=True)
    async with client:
        token = await client.aget_token()
        assert token, "No token retrieved"


def test_mock_sync():

    client = Herre(grant=MockGrant(),  no_temp=True)
    with client:
        token = client.get_token()
        assert token, "No token retrieved"
