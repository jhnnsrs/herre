from urllib.robotparser import RequestRate
from urllib.robotparser import RequestRate
import requests
import pytest
from herre import Herre
from herre.grants.oauth2.client_credentials import ClientCredentialsGrant
from .integration.utils import wait_for_http_response
from .utils import build_relative
from testcontainers.compose import DockerCompose
import subprocess
from functools import cached_property

class DockerV2Compose(DockerCompose):

    @cached_property
    def docker_cmd_comment(self):
        """Returns the base docker command by testing the docker compose api

        Returns:
            list[ſt]: _description_
        """
        return ["docker","compose"] if subprocess.run(["docker", "compose", "--help"], stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT).returncode == 0 else ["docker-compose"]

    def docker_compose_command(self):
        """
        Returns command parts used for the docker compose commands

        Returns
        -------
        list[str]
            The docker compose command parts
        """
        docker_compose_cmd = self.docker_cmd_comment
        for file in self.compose_file_names:
            docker_compose_cmd += ['-f', file]
        if self.env_file:
            docker_compose_cmd += ['--env-file', self.env_file]
        return docker_compose_cmd


@pytest.mark.integration
@pytest.fixture(scope="session")
def environment():


    with DockerV2Compose(
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
        grant=ClientCredentialsGrant(

        base_url="http://localhost:8008/o",
        client_id="DSNwVKbSmvKuIUln36FmpWNVE2KrbS2oRX0ke8PJ",
        client_secret="Gp3VldiWUmHgKkIxZjL2aEjVmNwnSyIGHWbQJo6bWMDoIUlBqvUyoGWUWAe6jI3KRXDOsD13gkYVCZR0po1BLFO9QT4lktKODHDs0GyyJEzmIjkpEOItfdCC4zIa3Qzu"),
      
    )
    with client:
        token = client.get_token()
        assert token, "No token retrieved"
