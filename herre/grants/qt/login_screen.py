import ssl
import certifi

from herre.grants.base import BaseGrant, BaseGrantProtocol
from herre.types import Token
from typing import List, Optional, Dict
import logging
from qtpy import QtWidgets, QtCore
from pydantic import BaseModel, Field

from koil.qt import QtCoro, QtFuture, QtRunner, qt_to_async, async_to_qt
from .errors import UserCancelledError
import asyncio
import aiohttp
from herre.grants.errors import GrantException
import json
from typing import runtime_checkable, Protocol
from herre.grants.stored_login import (
    UserStore,
    StoredUser,
)


logger = logging.getLogger(__name__)


class UserWidget(QtWidgets.QWidget):
    login_clicked = QtCore.Signal(object)
    logout_clicked = QtCore.Signal(object)

    def __init__(self, store: StoredUser, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.store = store

        self.user_label = QtWidgets.QLabel(store.user.username)
        self.user_label.mousePressEvent = self.on_clicked

        self.logout_button = QtWidgets.QPushButton("Logout")
        self.logout_button.clicked.connect(self.on_logout_clicked)

        self.hlayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hlayout)
        self.hlayout.addWidget(self.user_label)
        self.hlayout.addWidget(self.logout_button)

    def on_clicked(self, event):
        self.login_clicked.emit(self.store)

    def on_logout_clicked(self):
        self.logout_clicked.emit(self.store)


class ShouldWeSaveThisAsDefault(QtWidgets.QDialog):
    def __init__(self, stored: StoredUser = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f"Hi {stored.user}")

        self.qlabel = QtWidgets.QLabel(
            f"Do you want to save yourself as the default user?"
        )

        vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(vlayout)

        vlayout.addWidget(self.qlabel)

        hlayout = QtWidgets.QHBoxLayout()
        vlayout.addLayout(hlayout)

        self.yes_button = QtWidgets.QPushButton("Yes")
        self.no_button = QtWidgets.QPushButton("No")

        self.yes_button.clicked.connect(self.on_yes)
        self.no_button.clicked.connect(self.on_no)

        self.stored = stored

        hlayout.addWidget(self.yes_button)
        hlayout.addWidget(self.no_button)

    def on_yes(self):
        self.accept()

    def on_no(self):
        self.reject()


class LoginWidget(QtWidgets.QDialog):
    def __init__(self, settings: QtCore.QSettings, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vlayout = QtWidgets.QVBoxLayout()
        self.setWindowTitle("Login")
        self.resize(500, 500)
        self.setLayout(self.vlayout)

        self._future = None
        self.store = None
        self.settings = settings

        self.user_list_l = QtWidgets.QVBoxLayout()
        self.vlayout.addLayout(self.user_list_l)

        self.acloseme = qt_to_async(self.close, autoresolve=True)

        self.astart_selection = qt_to_async(self.start_selection)

        self.aask_save = qt_to_async(self.ask_save, autoresolve=True)

        self.delete_user = async_to_qt(self.adelete_user)
        self.delete_user.returned.connect(self.refresh_users)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.new_user_button = QtWidgets.QPushButton("New User")
        self.button_layout.addWidget(self.new_user_button)
        self.new_user_button.clicked.connect(self.on_new_user_clicked)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.button_layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        self.vlayout.addLayout(self.button_layout)

    def refresh_users(self):
        self.clearLayout(self.user_list_l)
        self.user_list_l.addWidget(QtWidgets.QLabel("Select User"))
        for users in self.users:
            widget = UserWidget(users)
            self.user_list_l.addWidget(widget)
            widget.login_clicked.connect(self.on_user_clicked)
            widget.logout_clicked.connect(self.on_user_deleted)

    def start_selection(self, future: QtFuture) -> None:
        self.refresh_users()
        self._future = future
        self.show()

    async def aselect_user(self, store: UserStore) -> None:
        self.store = store
        self.users = await self.store.aget_users()
        if self.users and self.settings.value("auto_login", False):
            return self.users[0]

        return await self.astart_selection()

    async def adelete_user(self, user: StoredUser) -> None:
        if self.store:
            await self.store.adelete_user(user.user)
        self.refresh_users()

    def ask_save(self, stored: StoredUser) -> bool:
        dialog = ShouldWeSaveThisAsDefault(parent=self, stored=stored)
        dialog.show()
        if dialog.exec_():
            return True
        else:
            return False

    def on_user_deleted(self, userStore: UserStore) -> None:
        self.users = [user for user in self.users if user.user.id != userStore.user.id]
        self.refresh_users()
        self.delete_user()
        # OPtimitics result but should be fine

    def clearLayout(self, layout) -> None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_cancel_clicked(self):
        self.close()

    def close(self) -> bool:
        if self._future:
            self._future.reject(UserCancelledError("The user cancelled the login"))
        return super().close()

    def on_new_user_clicked(self) -> None:
        if self._future:
            self._future.resolve(None)

    def on_user_clicked(self, user: StoredUser) -> None:
        if self._future:
            self._future.resolve(user)

    async def aclose(self) -> None:
        await self.acloseme()

    async def ashowexpired(self) -> None:
        print("show expired")

    async def ashow_welcome(self) -> None:
        print("show welcome")

    async def adestroy(self) -> None:
        await self.acloseme()

    async def ashould_we_save(self, store: StoredUser) -> bool:
        """Should ask the user if we should save the user"""
        return await self.aask_save(store)
