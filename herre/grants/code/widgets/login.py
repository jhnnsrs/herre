
from qtpy import QtCore
from qtpy.QtWidgets import QDialog, QVBoxLayout
from qtpy.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import logging
import os

logger = logging.getLogger(__name__)

class WebEnginePage(QWebEnginePage):

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        pass

class LoginWindow(QWebEngineView):
    """ A Login window for the OSF """

    def __init__(self, backend = None, tokenCallback=None):
        super(LoginWindow, self).__init__()
        self.state = None
        self.session = backend.session
        self.backend = backend

        auth_url, state = self.session.authorization_url(self.backend.auth_url)

        self.urlChanged.connect(self.check_URL)
        self.callback = tokenCallback
        self.setPage(WebEnginePage(self))
        self.load(QtCore.QUrl(auth_url))
        self.set_state(state)


    def set_state(self,state):
        self.state = state

    def check_URL(self, url: QtCore.QUrl):
        url = url.url()
        if url.startswith(self.backend.config.redirect_uri):
            try:
                token = self.session.fetch_token(self.backend.token_url, client_secret=self.backend.config.client_secret, authorization_response=url)
                if token: self.callback(token)
            except Exception as e:
                logger.exception(e)




class LoginDialog(QDialog):
    def __init__(self, backend = None, parent = None):
        super(LoginDialog, self).__init__(parent)
        self.setModal(True)
        layout = QVBoxLayout(self)

        # nice widget for editing the date
        self.webview = LoginWindow(backend=backend, tokenCallback=self.tokenReady)
        layout.addWidget(self.webview)

        self.token = None
        # OK and Cancel buttons

    def tokenReady(self, token):
        self.token = token
        self.webview.close() # NEEDS TO BE CALLED GOD DAMN IT
        self.accept()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getToken(backend = None, parent = None):
        dialog = LoginDialog(backend=backend, parent=parent)
        result = dialog.exec_()
        token = dialog.token
        return token, result == QDialog.Accepted