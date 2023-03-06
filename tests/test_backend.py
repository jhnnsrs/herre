from herre import Herre
from herre.grants.oauth2.client_credentials import ClientCredentialsGrant
from herre.grants.oauth2.session import OAuth2Session
from .utils import fake_token_generator
import pytest

@pytest.mark.asyncio
async def test_backend_mock_sync(monkeypatch):

    monkeypatch.setattr(OAuth2Session, "fetch_token", fake_token_generator)
    x = Herre(
        grant=ClientCredentialsGrant(
            base_url="http://localhost:8000/o",
            client_id="7JbA1yi2iQuqc6b4BUjtcYLBOB92V6fQfaE87EFF",
            client_secret="699FBMqg32oRcwQ4m06R8m5j1AWIoXiDnJ2UqEpAEtNoegtpmk69Wg3zD8Hk3C8pKws6QHzEhuuIU14LmUHq2qM12Pze37atxTslAnrOPBGv3PEKjKGMvcSguRW1JGZ6",
        ),
    )

    async with x:
        await x.aget_token()
