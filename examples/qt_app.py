from herre import Herre
from koil.qt import async_to_qt
from PyQt5 import QtWidgets
from herre.grants.oauth2.authorization_code import AuthorizationCodeGrant
from herre.grants.oauth2.redirecters.qt_login_view import WebViewRedirecter
import sys


class LoginWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grant = AuthorizationCodeGrant(
            base_url="https://github.com/login/oauth",
            token_path="access_token",
            client_id="dfdb2c594470db113659",
            scopes=[],
            append_trailing_slash=False,
            client_secret="bc59f1e3bc1ed0dcfb3548b457588f3b6e324764",
            redirecter=WebViewRedirecter(
                redirect_uri="http://127.0.0.1:6767/"
            ),  # this will open a
            # webview to display the login page
        )

        self.herre = Herre(
            grant=self.grant,
        )

        self.herre.enter()  # herre requires to be entered before it can be used

        self.login_task = async_to_qt(self.herre.aget_token)
        self.login_task.returned.connect(self.on_login_finished)
        self.login_task.errored.connect(self.on_login_error)

        self.login_button = QtWidgets.QPushButton("Login")
        self.greet_label = QtWidgets.QLabel("")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.greet_label)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.greet)

    def greet(self):
        self.login_task.run()

    def on_login_finished(self, token):
        self.greet_label.setText(f"Hello User")
        # do something with the token

    def on_login_error(self, error):
        self.greet_label.setText(f"Error: {error}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(
        ["", "--no-sandbox"]
    )  # you need to pass --no-sandbox to the
    # application if you are running it on linux (otherwise qtwebengine will not work)
    main_window = LoginWidget()

    main_window.show()
    sys.exit(app.exec())
