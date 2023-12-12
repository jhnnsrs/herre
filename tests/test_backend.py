from herre import Herre
from herre.grants.oauth2.client_credentials import ClientCredentialsGrant
from .utils import fake_token_generator
import pytest

@pytest.mark.asyncio
async def test_backend_mock_sync(valid_token_response):

    x = Herre(
        grant=ClientCredentialsGrant(
            base_url="http://localhost:8000/o",
            client_id="7JbA1yi2iQuqc6b4BUjtcYLBOB92V6fQfaE87EFF",
            client_secret="699FBMqg32oRcwQ4m06R8m5j1AWIoXiDnJ2UqEpAEtNoegtpmk69Wg3zD8Hk3C8pKws6QHzEhuuIU14LmUHq2qM12Pze37atxTslAnrOPBGv3PEKjKGMvcSguRW1JGZ6",
        ),
    )

    async with x:
        token = await x.aget_token()
        assert token == "mock_access_token", "Incorrect token retrieved"


@pytest.mark.asyncio
async def test_backend_mock_sync(failing_token_response):

    x = Herre(
        grant=ClientCredentialsGrant(
            base_url="http://localhost:8000/o",
            client_id="7JbA1yi2iQuqc6b4BUjtcYLBOB92V6fQfaE87EFF",
            client_secret="699FBMqg32oRcwQ4m06R8m5j1AWIoXiDnJ2UqEpAEtNoegtpmk69Wg3zD8Hk3C8pKws6QHzEhuuIU14LmUHq2qM12Pze37atxTslAnrOPBGv3PEKjKGMvcSguRW1JGZ6",
        ),
    )

    async with x:
        with pytest.raises(Exception):
            token = await x.aget_token()
