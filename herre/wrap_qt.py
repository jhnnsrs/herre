from .graphical import has_qt_error, has_qasync, QtWidgets, QSelectorEventLoop

def wrap_qt_in_loop(potential_app):
    assert not has_qt_error, f"You do not have the required Librarys installed {has_qt_error}"
    assert not has_qasync, f"You do not have the required Librarys installed {has_qasync}"

    assert isinstance(potential_app, QtWidgets.QApplication), "Passed down app is not an QApplication"
    return QSelectorEventLoop(potential_app)