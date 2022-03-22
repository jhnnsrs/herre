from distutils.command.config import config
from pydantic import Field
from herre.grants.base import BaseGrant
from herre.grants.refreshable import Refreshable
from herre.grants.openid import OpenIdUser
from herre.grants.session import OAuth2Session
from herre.herre import Herre
from herre.types import Token, User
from qtpy import QtWidgets
from koil.qt import QtCoro, QtFuture
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy import QtCore
from herre.grants.utils import build_authorize_url, build_token_url

from oauthlib.oauth2 import WebApplicationClient


class LoginWrapper(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.page()
        self.redirect_uri = None
        self.show_coro = QtCoro(self.initialize)
        self.urlChanged.connect(self._interceptUrl)

    def initialize(self, future: QtFuture, auth_url, redirect_uri):
        self.future = future
        self.redirect_uri = redirect_uri
        self.future = future

        self.setUrl(QtCore.QUrl(auth_url))
        self.show()

    def _interceptUrl(self, url):
        url_string = bytes(url.toEncoded()).decode()
        if self.redirect_uri:
            if url_string.startswith(self.redirect_uri):
                if self.future:
                    self.future.resolve(url_string)
                    self.close()


class WindowedGrant(BaseGrant, Refreshable, OpenIdUser):
    redirect_port: int = 6767
    redirect_host: str = "localhost"
    redirect_timeout: int = 40
    login_wrapper: LoginWrapper = Field(default_factory=LoginWrapper)

    async def afetch_token(self, herre: Herre) -> Token:

        redirect_uri = f"http://{self.redirect_host}:{self.redirect_port}"

        web_app_client = WebApplicationClient(
            herre.client_id.get_secret_value(),
            scope=herre.scope_delimiter.join(herre.scopes + ["openid"]),
        )

        async with OAuth2Session(
            herre.client_id.get_secret_value(),
            web_app_client,
            scope=herre.scope_delimiter.join(herre.scopes + ["openid"]),
            redirect_uri=redirect_uri,
        ) as session:

            auth_url, state = session.authorization_url(build_authorize_url(herre))

            path = await self.login_wrapper.show_coro.acall(auth_url, redirect_uri)

            token_dict = await session.fetch_token(
                build_token_url(herre),
                client_secret=herre.client_secret.get_secret_value(),
                authorization_response=path,
                state=state,
            )

            return Token(**token_dict)

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
        json_encoder = {
            QtWidgets.QWidget: lambda x: x.__class__.__name__,
        }
