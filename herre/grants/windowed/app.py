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
    def __init__(self, redirect_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.page()
        self.redirect_uri = redirect_uri
        self.urlChanged.connect(self._interceptUrl)

    def wait_for_redirect(self, auth_url, future):
        self.setUrl(QtCore.QUrl(auth_url))
        self.future = future

    def _interceptUrl(self, url):
        url_string = bytes(url.toEncoded()).decode()
        if url_string.startswith(self.redirect_uri):
            if self.future:
                self.future.resolve(url_string)
                self.close()


class WindowedGrant(BaseGrant, QtWidgets.QWidget, Refreshable, OpenIdUser):
    refreshable = True
    is_user_grant = False

    def __init__(
        self, *args, redirect_port=6767, redirect_timeout=40, **kwargs
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )
        self.show_coro = QtCoro(self.show)
        self.redirect_port = redirect_port
        self.redirect_timeout = redirect_timeout
        self.redirect_uri = f"http://localhost:{redirect_port}/"

        self.login_wrapper = LoginWrapper(self.redirect_uri)

    def show(self, future: QtFuture, auth_url):
        self.login_future = future
        self.login_wrapper.wait_for_redirect(auth_url, future)
        self.login_wrapper.show()

    async def afetch_token(self, herre: Herre) -> Token:
        print("We are binding to a future")
        web_app_client = WebApplicationClient(
            herre.client_id, scope=herre.scope_delimiter.join(herre.scopes + ["openid"])
        )

        async with OAuth2Session(
            herre.client_id,
            web_app_client,
            scope=herre.scope_delimiter.join(herre.scopes + ["openid"]),
            redirect_uri=self.redirect_uri,
        ) as session:

            auth_url, state = session.authorization_url(build_authorize_url(herre))

            path = await self.show_coro.acall(auth_url)

            token_dict = await session.fetch_token(
                build_token_url(herre),
                client_secret=herre.client_secret,
                authorization_response=path,
                state=state,
            )

            return Token(**token_dict)
