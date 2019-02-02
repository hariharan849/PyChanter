import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from resources.ui import findReplaceWidgetUI as _findReplaceWidgetUI


class FindReplaceWidget(QtWidgets.QWidget, _findReplaceWidgetUI.Ui_Form):
    def __init__(self, parent=None):
        super(FindReplaceWidget, self).__init__(parent)
        self.setupUi(self)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = FindReplaceWidget()
    myapp.show()
    sys.exit(app.exec_())