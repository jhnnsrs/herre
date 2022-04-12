from urllib.robotparser import RequestRate
from urllib.robotparser import RequestRate
import requests
from testcontainers.compose import DockerCompose
import pytest
from herre import Herre
from herre.grants.backend.app import BackendGrant
from .integration.utils import wait_for_http_response
from .utils import build_relative


@pytest.mark.integration
@pytest.fixture(scope="session")
def environment():
    with DockerCompose(
        filepath=build_relative("integration"),
        compose_file_name="docker-compose.yaml",
    ) as compose:
        wait_for_http_response("http://localhost:8008/ht", max_retries=5)
        yield


@pytest.mark.integration
def test_connection(environment):
    wait_for_http_response("http://localhost:8008/ht")
    response = requests.get("http://localhost:8008/ht")
    assert response.status_code == 200, "Did not get expected response code"


@pytest.mark.integration
def test_connection_again(environment):
    wait_for_http_response("http://localhost:8008/ht")
    response = requests.get("http://localhost:8008/ht")
    assert response.status_code == 200, "Did not get expected response code"


@pytest.mark.integration
def test_connection_x(environment):

    client = Herre(
        base_url="http://localhost:8008/o",
        grant=BackendGrant(),
        client_id="DSNwVKbSmvKuIUln36FmpWNVE2KrbS2oRX0ke8PJ",
        client_secret="Gp3VldiWUmHgKkIxZjL2aEjVmNwnSyIGHWbQJo6bWMDoIUlBqvUyoGWUWAe6jI3KRXDOsD13gkYVCZR0po1BLFO9QT4lktKODHDs0GyyJEzmIjkpEOItfdCC4zIa3Qzu",
        no_temp=True
    )
    with client:
        token = client.get_token()
        assert token, "No token retrieved"
