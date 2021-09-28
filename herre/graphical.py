
import asyncio


try:
    from qtpy import QtWidgets
    has_qt_error = False
        
except Exception as e:
    has_qt_error = e
    QtWidgets = None


try:
    from qtpy.QtWebEngineWidgets import QWebEngineView
    has_webview_error = False
        
except Exception as e:
    has_webview = False
    has_webview_error = e
    QWebEngineView = None

try:
    from qasync import QSelectorEventLoop
    has_qasync_error = False
    has_qasync = True
        
except Exception as e:
    has_qasync = False
    has_qasync_error = e
    QSelectorEventLoop = None



class GraphicalBackend:


    def __init__(self, parent=None) -> None:
        from herre.auth import get_current_herre
        self.herre = get_current_herre()
        self.parent = parent
        self.spawned_app = None


    def __enter__(self):
        global has_qt_error
        assert not has_qt_error, f"You cannot run with a Qt Backend if no QT Backend is installed. Please install PyQT5  or PySide {str(has_qt_error)}"

        if QtWidgets.QApplication.instance() is None:
            # if it does not exist then a QApplication is created
            self.spawned_app = QtWidgets.QApplication([])

        return self


    def __exit__(self, *args, **kwargs):
        if self.spawned_app: self.spawned_app.exit()


    async def __aenter__(self):
        assert QtWidgets.QApplication.instance() is not None, "You cannot call this Outside of an with_qt wrapped Application"
        assert isinstance(self.herre.loop, QSelectorEventLoop), "You cannot assign outside of an with_qt wrapped APplication"
        return self.__enter__()

    async def __aexit__(self, type, value, traceback):
        
        if type is not None:
            if issubclass(type, asyncio.CancelledError): 
                print("Raising cancellation")
                raise type(value).with_traceback(traceback)

            if issubclass(type, Exception):
                print(f"Raising exceütopm {type} {value} {traceback}")
                raise type(value).with_traceback(traceback)


            raise type(value).with_traceback(traceback)