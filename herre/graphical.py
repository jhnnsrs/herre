
import asyncio


try:
    from qtpy import QtWidgets
    has_qt = True
    qt_error = False
        
except Exception as e:
    has_qt = False
    qt_error = e
    QtWidgets = None


try:
    from qtpy.QtWebEngineWidgets import QWebEngineView
    has_webview = True
        
except Exception as e:
    has_webview = False
    web_view_error = e


class GraphicalBackend:


    def __init__(self, parent=None) -> None:
        self.parent = parent
        self.spawned_app = None


    def __enter__(self):
        global has_qt
        assert has_qt == True, f"You cannot run with a Qt Backend if no QT Backend is installed. Please install PyQT5 {str(has_qt)}"

        if QtWidgets.QApplication.instance() is None:
            # if it does not exist then a QApplication is created
            self.spawned_app = QtWidgets.QApplication([])

        return self


    def __exit__(self, *args, **kwargs):
        if self.spawned_app: self.spawned_app.exit()


    async def __aenter__(self):
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