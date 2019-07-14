"""
Generic PyQtUtils goes here
"""

import os as _os
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

        self.directoryValue = _QtWidgets.QLineEdit(self)
        self.directoryValue.setObjectName("lineEdit")
        self.directoryValue.setStyleSheet("border-radius: 8px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); ")
        self.directoryValue.setPlaceholderText(title)
        self._valueLayout.addWidget(self.directoryValue)

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
        self.setFixedSize(800, 122)
        self._dialogLayout = _QtWidgets.QVBoxLayout(self)
        self._dialogLayout.setObjectName("dialogLayout")

        self._valueLayout = _QtWidgets.QHBoxLayout()
        self._valueLayout.setObjectName("valueLayout")

        self.directoryValue = _QtWidgets.QLineEdit(self)
        self.directoryValue.setObjectName("lineEdit")
        self.directoryValue.setStyleSheet("border-radius: 8px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); ")
        self.directoryValue.setPlaceholderText('Browse Search Directory')
        self._valueLayout.addWidget(self.directoryValue)

        self.directoryButton = _QtWidgets.QToolButton(self)
        self.directoryButton.setText("Open Directory")
        self.directoryButton.setFixedSize(_QtCore.QSize(120, 34))
        self._valueLayout.addWidget(self.directoryButton)

        self._dialogLayout.addLayout(self._valueLayout)

        self._findLayout = _QtWidgets.QHBoxLayout()
        self._findLayout.setObjectName("findLayout")

        self.findValue = _QtWidgets.QLineEdit(self)
        self.findValue.setObjectName("findValue")
        self.findValue.setPlaceholderText('Enter Search Text')
        self.findValue.setStyleSheet(
            "border-radius: 8px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); ")
        self._findLayout.addWidget(self.findValue)
        self.findAllButton = _QtWidgets.QPushButton(self)
        self.findAllButton.setObjectName("findAllButton")
        self.findAllButton.setText("Find All")
        self.findAllButton.setFixedSize(_QtCore.QSize(120, 34))
        self._findLayout.addWidget(self.findAllButton)

        self._dialogLayout.addLayout(self._findLayout)
        self.setWindowTitle(title)

        self.directoryButton.clicked.connect(self._openDirectory)
        self.findAllButton.clicked.connect(self.close)

    def _openDirectory(self):
        directory = _QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            _os.path.dirname(self.parent().filePath) if self.parent().filePath else ''
        )
        if not directory:
            return
        self.directoryValue.setText(directory)

if __name__ == '__main__':
    import sys
    app = _QtWidgets.QApplication(sys.argv)
    try:
        console = FindAllDialog()
        console.show()
    except Exception as ex:
        print (ex)
        import traceback
        traceback.print_exc()
    sys.exit(app.exec_())