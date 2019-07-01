"""
Generic PyQtUtils goes here
"""

from PyQt5 import (
    QtCore as _QtCore,
    QtWidgets as _QtWidgets,
)


class InputDialog(_QtWidgets.QDialog):
    def __init__(self, title='', parent=None):
        super(InputDialog, self).__init__(parent)
        self.resize(400, 122)
        self._dialogLayout = _QtWidgets.QVBoxLayout(self)
        self._dialogLayout.setObjectName("dialogLayout")

        self._valueLayout = _QtWidgets.QHBoxLayout()
        self._valueLayout.setObjectName("valueLayout")

        self.label = _QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self._valueLayout.addWidget(self.label)

        self.lineValue = _QtWidgets.QLineEdit(self)
        self.lineValue.setObjectName("lineEdit")
        self.lineValue.setStyleSheet("border-radius: 8px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); ")
        self.lineValue.setPlaceholderText(title)
        self._valueLayout.addWidget(self.lineValue)

        self._dialogLayout.addLayout(self._valueLayout)

        self.buttonBox = _QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(_QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_QtWidgets.QDialogButtonBox.Cancel | _QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self._dialogLayout.addWidget(self.buttonBox)
        self.setWindowTitle(title)

        self.buttonBox.accepted.connect(self.close)
        self.buttonBox.rejected.connect(self.close)

class FindAllDialog(_QtWidgets.QDialog):
    def __init__(self, title='', parent=None):
        super(FindAllDialog, self).__init__(parent)
        self.resize(400, 122)
        self._dialogLayout = _QtWidgets.QVBoxLayout(self)
        self._dialogLayout.setObjectName("dialogLayout")

        self._valueLayout = _QtWidgets.QHBoxLayout()
        self._valueLayout.setObjectName("valueLayout")

        self.lineValue = _QtWidgets.QLineEdit(self)
        self.lineValue.setObjectName("lineEdit")
        self.lineValue.setStyleSheet("border-radius: 8px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); ")
        self.lineValue.setPlaceholderText(title)
        self._valueLayout.addWidget(self.lineValue)

        self.directoryButton = _QtWidgets.QToolButton(self)
        self.directoryButton.setText("Open Directory")
        self._valueLayout.addWidget(self.directoryButton)

        self._dialogLayout.addLayout(self._valueLayout)

        self.buttonBox = _QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(_QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_QtWidgets.QDialogButtonBox.Cancel | _QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self._dialogLayout.addWidget(self.buttonBox)
        self.setWindowTitle(title)

        self.directoryButton.clicked.connect(self._openDirectory)
        self.buttonBox.accepted.connect(self.close)
        self.buttonBox.rejected.connect(self.close)

    def _openDirectory(self):
        directory = _QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            self.parent().recentDirectory
        )
        if not directory:
            return
        self.lineValue.setText(directory)
        self.adjustSize()

if __name__ == '__main__':
    import sys
    app = _QtWidgets.QApplication(sys.argv)
    try:
        console = InputDialog()
        console.show()
    except Exception as ex:
        print (ex)
        import traceback
        traceback.print_exc()
    sys.exit(app.exec_())