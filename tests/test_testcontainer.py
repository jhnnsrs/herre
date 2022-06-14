import pytest
from testcontainers.compose import DockerCompose
from .utils import build_relative

@pytest.mark.integration
def test_environment():
    """This should only test if we can use testcontainers.compose.DockerCompose
    to start a container.

    If this fails, we can't use testcontainers.compose.DockerCompose to start
    and the problem does not lie in herre.
    """
    with DockerCompose(
        filepath=build_relative("integration"),
        compose_file_name="hello-compose.yaml",
    ) as compose:
        assert True, "We should be here"
