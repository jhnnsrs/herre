from herre.herre import Herre
from herre.grants.windowed import WindowedGrant
from koil.qt import QtKoil
from qtpy import QtWidgets
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.koil = QtKoil()
        self.herre = Herre(
            base_url="http://localhost:8000/o",
            grant=WindowedGrant(),
            client_id="UGqhHa2OS8NmTRjkVg8WKOWczYqkDVuK61yCueuO",
            client_secret="3oosB6FoC2iGASI8tkN16S8mPtlIvhqetvG5EOOJcLkn3txggTRxdp35G23CkNmvEY6fQXIXHaSzTa9Jb5Rk1hxWx0Fey0iUeOv2ZN568Z9z14kUbUbm4QQ1nacUW1gD",
        )
        self.setWindowTitle("My App")
        self.button = QtWidgets.QPushButton("Press Me!")
        self.herre.connect()

        self.login_task = self.herre.get_token(as_task=True)
        self.login_task.returned.connect(
            lambda: self.button.setText(f"Logged in as {self.herre.user}!")
        )

        self.button.clicked.connect(self.login)

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)

    def login(self):
        self.login_task.run()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
