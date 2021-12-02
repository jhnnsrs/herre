from herre import Herre


async def test_client_credentials():

    client = Herre(config_path="tests/configs/bergen.yaml")
    await client.alogin()
    assert client.headers is not None

