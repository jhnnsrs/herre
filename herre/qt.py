from herre import Herre
from qtpy import QtCore, QtWidgets


class QtHerre(Herre, QtWidgets.QWidget):
    login_signal = QtCore.Signal()
    logout_signal = QtCore.Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def alogin(self, **kwargs):
        nana = await super().alogin(**kwargs)
        self.login_signal.emit()
        return nana

    async def alogout(self, **kwargs):
        nana = await super().alogout(**kwargs)
        self.logout_signal.emit()
        return nana
