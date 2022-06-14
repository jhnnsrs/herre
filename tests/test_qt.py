import time

import pytest
from herre import Herre
from herre.grants.test.app import MockGrant
from koil.qt import QtKoil, QtRunner
from PyQt5 import QtWidgets, QtCore
from herre.grants.windowed.app import LoginWrapper, WindowedGrant
from herre import Herre, utils
from herre.grants.backend.app import BackendGrant
from herre.grants.code_server.app import AuthorizationCodeServerGrant
from herre.grants.test.app import MockGrant
from herre.grants.session import OAuth2Session
from herre.types import User


async def fake_token_generator(*args, **kwargs):
    return {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
    }


async def fake_user_generator(*args, **kwargs):
    return User(sub="fake_user")


class QtHerreWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.koil = QtKoil(parent=self)
        self.koil.enter()

        self.grant = WindowedGrant()

        self.herre = Herre(
            base_url="http://localhost:8000/o",
            grant=self.grant,
            client_id="UGqhHa2OS8NmTRjkVg8WKOWczYqkDVuK61yCueuO",
            client_secret="3oosB6FoC2iGASI8tkN16S8mPtlIvhqetvG5EOOJcLkn3txggTRxdp35G23CkNmvEY6fQXIXHaSzTa9Jb5Rk1hxWx0Fey0iUeOv2ZN568Z9z14kUbUbm4QQ1nacUW1gD",
            no_temp=True,
        )

        self.herre.enter()

        self.login_task = QtRunner(self.herre.alogin)

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
def test_fetch_from_windowed_grant(qtbot, monkeypatch):
    """Tests if we can call a task from a koil widget."""

    monkeypatch.setattr(
        LoginWrapper,
        "initialize",
        lambda self, future, auth, redirect: future.resolve("path"),
    )

    monkeypatch.setattr(OAuth2Session, "fetch_token", fake_token_generator)
    monkeypatch.setattr(WindowedGrant, "afetch_user", fake_user_generator)

    widget = QtHerreWidget()
    qtbot.addWidget(widget)
    # click in the Greet button and make sure it updates the appropriate label
    with qtbot.waitSignal(widget.login_task.returned) as b:
        qtbot.mouseClick(widget.button_greet, QtCore.Qt.LeftButton)

        print(b)
