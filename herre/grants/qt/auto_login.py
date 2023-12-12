from qtpy import QtWidgets

from koil.qt import qt_to_async

from herre.grants.auto_login import (
    StoredUser,
)


class ShouldWeSaveThisAsDefault(QtWidgets.QDialog):
    """A dialog that asks the user if they want to save the user as the default user."""

    def __init__(self, stored: StoredUser, *args, **kwargs) -> None:
        """Creates a new ShouldWeSaveThisAsDefault dialog"""
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f"Hi {stored.user.username}")

        self.qlabel = QtWidgets.QLabel(
            "Do you want to save yourself as the default user?"
        )

        vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(vlayout)

        vlayout.addWidget(self.qlabel)

        hlayout = QtWidgets.QHBoxLayout()
        vlayout.addLayout(hlayout)

        self.yes_button = QtWidgets.QPushButton("Yes")
        self.no_button = QtWidgets.QPushButton("No")

        self.yes_button.clicked.connect(self._on_yes)
        self.no_button.clicked.connect(self._on_no)

        self.stored = stored

        hlayout.addWidget(self.yes_button)
        hlayout.addWidget(self.no_button)

    def _on_yes(self) -> None:
        self.accept()

    def _on_no(self) -> None:
        self.reject()


class AutoLoginWidget(QtWidgets.QWidget):
    """A Qt widget for auto login.

    This widget can be used by the AutoLoginGrant to show the login widget
    and ask the user if they want to save the user.

    """

    def __init__(self, *args, **kwargs) -> None:
        """Creates a new AutoLoginWidget"""
        super().__init__(*args, **kwargs)

        self.ashould_we = qt_to_async(self._should_we, autoresolve=True)

    def _should_we(self, stored: StoredUser) -> bool:
        dialog = ShouldWeSaveThisAsDefault(stored, parent=self)
        dialog.exec_()
        return dialog.result() == QtWidgets.QDialog.Accepted

    async def ashould_we_save(self, store: StoredUser) -> bool:
        """Should ask the user if we should save the user"""
        return await self.ashould_we(store)
