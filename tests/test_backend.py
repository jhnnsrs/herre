from herre import Herre
from herre.grants.backend.app import BackendGrant
from herre.grants.test.app import MockGrant
from herre.grants.session import OAuth2Session
from tests.herretest.utils import fake_token_generator, fake_user_generator


async def test_backend_mock_sync(monkeypatch):

    monkeypatch.setattr(OAuth2Session, "fetch_token", fake_token_generator)
    monkeypatch.setattr(BackendGrant, "afetch_user", fake_user_generator)
    x = Herre(
        base_url="http://localhost:8000/o",
        grant=BackendGrant(),
        client_id="7JbA1yi2iQuqc6b4BUjtcYLBOB92V6fQfaE87EFF",
        client_secret="699FBMqg32oRcwQ4m06R8m5j1AWIoXiDnJ2UqEpAEtNoegtpmk69Wg3zD8Hk3C8pKws6QHzEhuuIU14LmUHq2qM12Pze37atxTslAnrOPBGv3PEKjKGMvcSguRW1JGZ6",
        no_temp=True,
    )

    async with x:
        await x.aget_token()
