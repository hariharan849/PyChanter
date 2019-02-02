import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from resources.ui import inputDialogUI as _inputDialogUI


class InputDialog(QtWidgets.QDialog, _inputDialogUI.Ui_Dialog):
    def __init__(self, title='', parent=None):
        super(InputDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        frame = self.frameGeometry()
        geometry = QtWidgets.QDesktopWidget().availableGeometry()
        frame.moveCenter(geometry.center())
        self.move(frame.topLeft())
        self.setModal(True)
        self.lineValue.setPlaceholderText(title)
        self.setWindowTitle(title)
        self.show()

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Return:
            self.close()
        super(InputDialog, self).keyPressEvent(ev)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = InputDialog()
    myapp.show()
    sys.exit(app.exec_())