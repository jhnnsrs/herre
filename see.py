import sys
from qtpy import QtWidgets
from koil.qt import QtKoil, QtTask
from herre.grants.windowed.app import LoginWrapper, WindowedGrant
from herre import Herre


class QtHerreWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.koil = QtKoil()

        self.grant = WindowedGrant()

        self.herre = Herre(
            base_url="http://localhost:8000/o",
            grant=self.grant,
            client_id="UGqhHa2OS8NmTRjkVg8WKOWczYqkDVuK61yCueuO",
            client_secret="3oosB6FoC2iGASI8tkN16S8mPtlIvhqetvG5EOOJcLkn3txggTRxdp35G23CkNmvEY6fQXIXHaSzTa9Jb5Rk1hxWx0Fey0iUeOv2ZN568Z9z14kUbUbm4QQ1nacUW1gD",
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
