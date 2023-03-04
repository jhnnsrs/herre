import sys
from qtpy import QtWidgets
from koil.qt import QtKoil, QtTask
from herre.grants.windowed.app import WindowedGrant
from herre import Herre


class QtHerreWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.koil = QtKoil()

        self.grant = WindowedGrant()

        self.herre = Herre(
            base_url="http://localhost:8000/o",
            grant=self.grant,
            client_id="Zvc8fwLMMINjcAxoaTBG2L6ATlV746D3Zc4T4Wiu",
            client_secret="bPDJKpvrZkhqsIvytwJuuLv8SEKeybPaPeMVpIRtdByLUERtyES2v18Dm38PUbVO0myUFAwLzwyWjo4jk91Yrhlfn51DPXN7MxYCIRedXSaNabvINv8EKv3kcWSY8Wos",
        )

        self.herre.connect()

        self.login_task = QtTask(self.herre.alogin)

        self.button_greet = QtWidgets.QPushButton("Greet")
        self.greet_label = QtWidgets.QLabel("")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button_greet)
        layout.addWidget(self.greet_label)

        self.setLayout(layout)

        self.button_greet.clicked.connect(self.greet)

    def greet(self):
        self.login_task.run()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtHerreWidget()

    window.show()
    sys.exit(app.exec())
