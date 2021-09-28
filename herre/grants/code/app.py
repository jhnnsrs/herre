from herre.graphical import GraphicalBackend, has_webview_error
from herre.console.context import console, get_current_console
from herre.grants.base import BaseGrant
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib.oauth2_session import OAuth2Session
from aiohttp import ClientSession
import requests

class AuthorizationCodeGrant(BaseGrant):
    refreshable = True

    def fetchToken(self, **kwargs):

        self.web_app_client = WebApplicationClient(self.config.client_id, scope=self.scope)

        # Create an OAuth2 session for the OSF
        self.session = OAuth2Session(
            self.config.client_id, 
            self.web_app_client,
            scope=self.scope, 
            redirect_uri=self.config.redirect_uri,
            
        )

        with GraphicalBackend():
            assert not has_webview_error, "Please install 'PyQtWebEngine' if you want to use the Implicit Flow"
            from herre.grants.code.widgets.login import LoginDialog
            self.token, accepted = LoginDialog.getToken(backend=self)

        return accepted

   

