import logging
from pydantic import BaseModel
from herre.models import TokenRequest
import urllib.parse

logger = logging.getLogger(__name__)


class MockRedirecter(BaseModel):
    """A simple webserver that will listen for a redirect from the OSF and return the path"""

    code: str
    """ The code to return """
    redirect_port: int = 6767
    redirect_timeout: int = 40
    redirect_host: str = "127.0.0.1"
    redirect_protocol: str = "http"
    redirect_path: str = "/"

    async def aget_redirect_uri(self, token_request: TokenRequest) -> str:
        """Retrieves the redirect uri

        This function will retrieve the redirect uri from the RedirectWaiter.
        This function has to be implemented by the user.

        """

        return f"{self.redirect_protocol}://{self.redirect_host}:{self.redirect_port}{self.redirect_path}"

    async def astart(
        self,
        auth_url: str,
    ) -> str:
        """Awaits a redirect

        This has to be implemented by a user

        """
        parsed_url = urllib.parse.urlparse(auth_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Extract the redirect URI and state parameter
        redirect_uri_param = query_params.get("redirect_uri", [""])[0]
        state = query_params.get("state", [""])[0]

        if not redirect_uri_param:
            raise ValueError("Redirect URI not found in the authorization URL.")

        # Reconstruct the redirect URI with the code and state
        redirect_uri_components = list(urllib.parse.urlparse(redirect_uri_param))
        redirect_query_params = {"code": self.code}
        if state:
            redirect_query_params["state"] = state

        redirect_uri_components[4] = urllib.parse.urlencode(
            redirect_query_params
        )  # Set the query component
        return urllib.parse.urlunparse(redirect_uri_components)
