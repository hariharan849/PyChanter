# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'findReplaceWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(838, 185)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.dockWidget = QtWidgets.QDockWidget(Form)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.findValue = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.findValue.setObjectName("findValue")
        self.gridLayout_2.addWidget(self.findValue, 0, 0, 1, 1)
        self.findButton = QtWidgets.QToolButton(self.dockWidgetContents)
        self.findButton.setObjectName("findButton")
        self.gridLayout_2.addWidget(self.findButton, 0, 1, 1, 1)
        self.findAllButton = QtWidgets.QToolButton(self.dockWidgetContents)
        self.findAllButton.setObjectName("findAllButton")
        self.gridLayout_2.addWidget(self.findAllButton, 0, 2, 1, 1)
        self.replaceValue = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.replaceValue.setObjectName("replaceValue")
        self.gridLayout_2.addWidget(self.replaceValue, 1, 0, 1, 1)
        self.replaceButton = QtWidgets.QToolButton(self.dockWidgetContents)
        self.replaceButton.setObjectName("replaceButton")
        self.gridLayout_2.addWidget(self.replaceButton, 1, 1, 1, 1)
        self.replaceAllButton = QtWidgets.QToolButton(self.dockWidgetContents)
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.gridLayout_2.addWidget(self.replaceAllButton, 1, 2, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.gridLayout.addWidget(self.dockWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.findButton.setText(_translate("Form", "Find"))
        self.findAllButton.setText(_translate("Form", "Find All"))
        self.replaceButton.setText(_translate("Form", "Replace"))
        self.replaceAllButton.setText(_translate("Form", "Replace All"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

