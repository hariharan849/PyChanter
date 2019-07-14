# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\findAllDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 96)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.fileBrowsetValue = QtWidgets.QLineEdit(Dialog)
        self.fileBrowsetValue.setObjectName("fileBrowsetValue")
        self.gridLayout.addWidget(self.fileBrowsetValue, 0, 0, 1, 1)
        self.browseButton = QtWidgets.QToolButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browseButton.sizePolicy().hasHeightForWidth())
        self.browseButton.setSizePolicy(sizePolicy)
        self.browseButton.setMinimumSize(QtCore.QSize(0, 34))
        self.browseButton.setObjectName("browseButton")
        self.gridLayout.addWidget(self.browseButton, 0, 1, 1, 1)
        self.findValue = QtWidgets.QLineEdit(Dialog)
        self.findValue.setObjectName("findValue")
        self.gridLayout.addWidget(self.findValue, 1, 0, 1, 1)
        self.findAllButton = QtWidgets.QPushButton(Dialog)
        self.findAllButton.setObjectName("findAllButton")
        self.gridLayout.addWidget(self.findAllButton, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.fileBrowsetValue.setPlaceholderText(_translate("Dialog", "Browse Search Directory"))
        self.browseButton.setText(_translate("Dialog", "Browse"))
        self.findValue.setPlaceholderText(_translate("Dialog", "Search Text"))
        self.findAllButton.setText(_translate("Dialog", "Find All"))

