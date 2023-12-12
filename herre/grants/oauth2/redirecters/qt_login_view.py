from herre.models import TokenRequest
from koil.qt import qt_to_async, QtFuture
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy import QtCore


class WebViewRedirecter(QWebEngineView):
    """A qt webengine view that can be used to login to a oauth2 provider

    This class is used to login to a oauth2 provider, when using the authorization code grant,
    but without a webserver. This class will open a webview, and wait for the user to login.
    When the user is logged in, the user will be redirected to the redirect_uri.
    This redirect_uri will be intercepted, and the code will be returned to the caller.


    """

    def __init__(
        self, *args, redirect_uri: str = "http://localhost:4893/", **kwargs
    ) -> None:
        """Creates a new WebViewRedirecter

        This function will create a new LoginWrapper, and initialize the webview.

        Parameters
        ----------
        redirect_uri : str
            The redirect_uri to intercept (you shoud own this uri)

        **kwargs
            The arguments to pass to the webview

        """
        super().__init__(*args, **kwargs)
        self.name = self.page()
        self.redirect_uri = redirect_uri
        self.future = None
        self.show_coro = qt_to_async(self.initialize)

    def initialize(self, future: QtFuture, auth_url: str) -> None:
        """Initializes the LoginWrapper

        This function will initialize the LoginWrapper, and open the webview.
        It will also set the future to resolve when the user is logged in.

        Parameters
        ----------
        future : QtFuture
            The future to resolve when the user is logged in
        auth_url : str
            The url to login to
        redirect_uri : str
            The redirect_uri to intercept
        """
        self.future = future

        self.load(QtCore.QUrl(auth_url))
        self.show()
        self.urlChanged.connect(self.on_urlChanged)

    def on_urlChanged(self, url: QtCore.QUrl) -> None:
        """Intercepts a url

        This function will intercept a url, and resolve the future when the url
        starts with the redirect_uri
        """
        url_string = bytes(url.toEncoded()).decode()
        if self.redirect_uri:
            if url_string.startswith(self.redirect_uri):
                if self.future:
                    self.future.resolve(url_string)
                    self.close()
                else:
                    pass

    async def astart(self, auth_url: str) -> str:
        """Starts the LoginWrapper

        This function will start the LoginWrapper, and return the code when the user is logged in.

        Parameters
        ----------
        auth_url : str
            The url to login to
        redirect_uri : str
            The redirect_uri to intercept

        Returns
        -------
        str
            The redirect_uri with the code
        """
        return await self.show_coro(auth_url)

    async def aget_redirect_uri(self, token_request: TokenRequest) -> str:
        """Retrieves the redirect uri

        This function will retrieve the redirect uri from the RedirectWaiter.
        This function has to be implemented by the user.

        """

        return self.redirect_uri
