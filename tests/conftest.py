import requests
import pytest
from herre import Herre
from herre.grants.oauth2.client_credentials import ClientCredentialsGrant
from .utils import build_relative
from testcontainers.compose import DockerCompose
import subprocess
from functools import cached_property
import pytest
from aioresponses import aioresponses


@pytest.fixture
def cc_token_response():
    with aioresponses() as m:
        m.post(
            "http://localhost:8000/o/token/",
            status=200,
            payload={"access_token": "mock_access_token", "token_type": "Bearer"},
        )

        yield m


@pytest.fixture
def failing_token_response():
    with aioresponses() as m:
        m.post(
            "http://localhost:8000/o/token/",
            status=400,
            payload={"status": "Failed"},
        )

        yield m


@pytest.fixture
def valid_token_response():
    with aioresponses() as m:
        m.post(
            "http://localhost:8000/o/token/",
            status=200,
            payload={"access_token": "mock_access_token", "token_type": "Bearer"},
        )

        yield m
