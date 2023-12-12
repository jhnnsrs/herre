import pytest
from herre import Herre
from koil.qt import async_to_qt, QtRunner
from koil.composition.qt import QtPedanticKoil
from PyQt5 import QtWidgets, QtCore
from herre.grants.oauth2.authorization_code import AuthorizationCodeGrant
from herre.grants.oauth2.redirecters.qt_login_view import WebViewRedirecter
from tests.utils import wait_for_qttask, loggin_wrapper_result


class QtHerreWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grant = AuthorizationCodeGrant(
            base_url="http://localhost:8000/o",
            client_id="UGqhHa2OS8NmTRjkVg8WKOWczYqkDVuK61yCueuO",
            client_secret="3oosB6FoC2iGASI8tkN16S8mPtlIvhqetvG5EOOJcLkn3txggTRxdp35G23CkNmvEY6fQXIXHaSzTa9Jb5Rk1hxWx0Fey0iUeOv2ZN568Z9z14kUbUbm4QQ1nacUW1gD",
            redirecter=WebViewRedirecter(parent=self),
        )

        self.herre = Herre(
            grant=self.grant,
        )

        self.herre.enter()

        self.login_task = QtRunner(self.herre.aget_token)

        self.button_greet = QtWidgets.QPushButton("Greet")
        self.greet_label = QtWidgets.QLabel("")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button_greet)
        layout.addWidget(self.greet_label)

        self.setLayout(layout)

        self.button_greet.clicked.connect(self.greet)

    def greet(self):
        self.login_task.run()


@pytest.mark.qt
def test_fetch_from_windowed_grant(qtbot, monkeypatch, valid_token_response):
    """Tests if we can call a task from a koil widget."""

    monkeypatch.setattr(
        WebViewRedirecter,
        "astart",
        loggin_wrapper_result,
    )

    widget = QtHerreWidget()
    qtbot.addWidget(widget)
    # click in the Greet button and make sure it updates the appropriate label

    result = wait_for_qttask(
        qtbot,
        widget.login_task,
        lambda qtbot: qtbot.mouseClick(widget.button_greet, QtCore.Qt.LeftButton),
    )

    assert result == "mock_access_token", "Incorrect token retrieved"
