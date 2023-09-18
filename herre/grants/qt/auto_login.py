import ssl
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
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


class ShouldWeSaveThisAsDefault(QtWidgets.QDialog):
    def __init__(self, stored: StoredUser = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f"Hi {stored.user.username}")

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


class AutoLoginWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.ashould_we = qt_to_async(self.should_we, autoresolve=True)

    def should_we(self, stored: StoredUser) -> bool:
        dialog = ShouldWeSaveThisAsDefault(stored, parent=self)
        dialog.exec_()
        return dialog.result() == QtWidgets.QDialog.Accepted

    async def ashould_we_save(self, store: StoredUser) -> bool:
        """Should ask the user if we should save the user"""
        return await self.ashould_we(store)
