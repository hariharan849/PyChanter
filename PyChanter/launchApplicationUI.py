# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\launchApplication.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(859, 665)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.editorLayout = QtWidgets.QVBoxLayout()
        self.editorLayout.setObjectName("editorLayout")
        self.editorTabWidget = CustomEditorTab(self.centralwidget)
        self.editorTabWidget.setTabsClosable(True)
        self.editorTabWidget.setObjectName("editorTabWidget")
        self.editorLayout.addWidget(self.editorTabWidget)
        self.findReplaceWidget = QtWidgets.QDockWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findReplaceWidget.sizePolicy().hasHeightForWidth())
        self.findReplaceWidget.setSizePolicy(sizePolicy)
        self.findReplaceWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.findReplaceWidget.setObjectName("findReplaceWidget")
        self.findDockWidgetContents = QtWidgets.QWidget()
        self.findDockWidgetContents.setObjectName("findDockWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.findDockWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.findValue = QtWidgets.QLineEdit(self.findDockWidgetContents)
        self.findValue.setStyleSheet("border-radius: 8px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); ")
        self.findValue.setObjectName("findValue")
        self.gridLayout_3.addWidget(self.findValue, 0, 0, 1, 1)
        self.findForwardButton = QtWidgets.QToolButton(self.findDockWidgetContents)
        self.findForwardButton.setMinimumSize(QtCore.QSize(100, 0))
        self.findForwardButton.setObjectName("findForwardButton")
        self.gridLayout_3.addWidget(self.findForwardButton, 0, 1, 1, 1)
        self.findPrevButton = QtWidgets.QToolButton(self.findDockWidgetContents)
        self.findPrevButton.setMinimumSize(QtCore.QSize(100, 0))
        self.findPrevButton.setObjectName("findPrevButton")
        self.gridLayout_3.addWidget(self.findPrevButton, 0, 2, 1, 1)
        self.replaceValue = QtWidgets.QLineEdit(self.findDockWidgetContents)
        self.replaceValue.setStyleSheet("border-radius: 8px; color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); ")
        self.replaceValue.setObjectName("replaceValue")
        self.gridLayout_3.addWidget(self.replaceValue, 1, 0, 1, 1)
        self.replaceButton = QtWidgets.QToolButton(self.findDockWidgetContents)
        self.replaceButton.setMinimumSize(QtCore.QSize(100, 0))
        self.replaceButton.setObjectName("replaceButton")
        self.gridLayout_3.addWidget(self.replaceButton, 1, 1, 1, 1)
        self.replaceAllButton = QtWidgets.QToolButton(self.findDockWidgetContents)
        self.replaceAllButton.setMinimumSize(QtCore.QSize(100, 0))
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.gridLayout_3.addWidget(self.replaceAllButton, 1, 2, 1, 1)
        self.findReplaceWidget.setWidget(self.findDockWidgetContents)
        self.editorLayout.addWidget(self.findReplaceWidget)
        self.gridLayout_2.addLayout(self.editorLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 859, 31))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuFind = QtWidgets.QMenu(self.menubar)
        self.menuFind.setObjectName("menuFind")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.directoryTreeDockWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.directoryTreeDockWidget.sizePolicy().hasHeightForWidth())
        self.directoryTreeDockWidget.setSizePolicy(sizePolicy)
        self.directoryTreeDockWidget.setMinimumSize(QtCore.QSize(324, 297))
        self.directoryTreeDockWidget.setObjectName("directoryTreeDockWidget")
        self.directoryDockWidgetContents = QtWidgets.QWidget()
        self.directoryDockWidgetContents.setObjectName("directoryDockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.directoryDockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.directoryTreeView = DirectoryTree(self.directoryDockWidgetContents)
        self.directoryTreeView.setObjectName("directoryTreeView")
        self.gridLayout.addWidget(self.directoryTreeView, 0, 0, 1, 1)
        self.directoryTreeDockWidget.setWidget(self.directoryDockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.directoryTreeDockWidget)
        self.interpreterDockWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.interpreterDockWidget.sizePolicy().hasHeightForWidth())
        self.interpreterDockWidget.setSizePolicy(sizePolicy)
        self.interpreterDockWidget.setMinimumSize(QtCore.QSize(105, 150))
        self.interpreterDockWidget.setObjectName("interpreterDockWidget")
        self.interpreterDockWidgetContents = QtWidgets.QWidget()
        self.interpreterDockWidgetContents.setObjectName("interpreterDockWidgetContents")
        self.interpreterGridLayout = QtWidgets.QGridLayout(self.interpreterDockWidgetContents)
        self.interpreterGridLayout.setObjectName("interpreterGridLayout")
        self.interpreterWidget = InterpreterWidget(self.interpreterDockWidgetContents)
        self.interpreterWidget.setGeometry(QtCore.QRect(13, 13, 774, 91))
        self.interpreterWidget.setObjectName("interpreterWidget")
        self.interpreterGridLayout.addWidget(self.interpreterWidget)
        self.interpreterDockWidget.setWidget(self.interpreterDockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.interpreterDockWidget)
        self.moduleTreeDockWidget = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moduleTreeDockWidget.sizePolicy().hasHeightForWidth())
        self.moduleTreeDockWidget.setSizePolicy(sizePolicy)
        self.moduleTreeDockWidget.setMinimumSize(QtCore.QSize(324, 297))
        self.moduleTreeDockWidget.setObjectName("moduleTreeDockWidget")
        self.moduleDockWidgetContents = QtWidgets.QWidget()
        self.moduleDockWidgetContents.setObjectName("moduleDockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.moduleDockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.moduleTreeView = PythonModuleInfo(self.moduleDockWidgetContents)
        self.moduleTreeView.setObjectName("moduleTreeView")
        self.gridLayout.addWidget(self.moduleTreeView, 0, 0, 1, 1)
        self.moduleTreeDockWidget.setWidget(self.moduleDockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.moduleTreeDockWidget)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen_Directory = QtWidgets.QAction(MainWindow)
        self.actionOpen_Directory.setObjectName("actionOpen_Directory")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionCloseTab = QtWidgets.QAction(MainWindow)
        self.actionCloseTab.setObjectName("actionCloseTab")
        self.actionCloseAllTab = QtWidgets.QAction(MainWindow)
        self.actionCloseAllTab.setObjectName("actionCloseAllTab")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionRecent = QtWidgets.QAction(MainWindow)
        self.actionRecent.setObjectName("actionRecent")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionIndent = QtWidgets.QAction(MainWindow)
        self.actionIndent.setObjectName("actionIndent")
        self.actionUnIndent = QtWidgets.QAction(MainWindow)
        self.actionUnIndent.setObjectName("actionUnIndent")
        self.actionLineCut = QtWidgets.QAction(MainWindow)
        self.actionLineCut.setObjectName("actionLineCut")
        self.actionLineCopy = QtWidgets.QAction(MainWindow)
        self.actionLineCopy.setObjectName("actionLineCopy")
        self.actionLinePaste = QtWidgets.QAction(MainWindow)
        self.actionLinePaste.setObjectName("actionLinePaste")
        self.actionLineDuplicate = QtWidgets.QAction(MainWindow)
        self.actionLineDuplicate.setObjectName("actionLineDuplicate")
        self.actionLineTranspose = QtWidgets.QAction(MainWindow)
        self.actionLineTranspose.setObjectName("actionLineTranspose")
        self.actionCommentUncomment = QtWidgets.QAction(MainWindow)
        self.actionCommentUncomment.setObjectName("actionCommentUncomment")
        self.actionGotoLine = QtWidgets.QAction(MainWindow)
        self.actionGotoLine.setObjectName("actionGotoLine")
        self.actionHighlight = QtWidgets.QAction(MainWindow)
        self.actionHighlight.setObjectName("actionHighlight")
        self.actionUpperCase = QtWidgets.QAction(MainWindow)
        self.actionUpperCase.setObjectName("actionUpperCase")
        self.actionLowerCase = QtWidgets.QAction(MainWindow)
        self.actionLowerCase.setObjectName("actionLowerCase")
        self.actionCamelCase = QtWidgets.QAction(MainWindow)
        self.actionCamelCase.setObjectName("actionCamelCase")
        self.actionFind = QtWidgets.QAction(MainWindow)
        self.actionFind.setObjectName("actionFind")
        self.actionFindAll = QtWidgets.QAction(MainWindow)
        self.actionFindAll.setObjectName("actionFindAll")
        self.actionReplace = QtWidgets.QAction(MainWindow)
        self.actionReplace.setObjectName("actionReplace")
        self.actionReplaceAll = QtWidgets.QAction(MainWindow)
        self.actionReplaceAll.setObjectName("actionReplaceAll")
        self.actionLineUp = QtWidgets.QAction(MainWindow)
        self.actionLineUp.setObjectName("actionLineUp")
        self.actionLineDown = QtWidgets.QAction(MainWindow)
        self.actionLineDown.setObjectName("actionLineDown")
        self.actionFoldAll = QtWidgets.QAction(MainWindow)
        self.actionFoldAll.setObjectName("actionFoldAll")
        self.actionCurrentFold = QtWidgets.QAction(MainWindow)
        self.actionCurrentFold.setObjectName("actionCurrentFold")
        self.actionUnFold = QtWidgets.QAction(MainWindow)
        self.actionUnFold.setObjectName("actionUnFold")
        self.actionPythonConsole = QtWidgets.QAction(MainWindow)
        self.actionPythonConsole.setObjectName("actionPythonConsole")
        self.actionRunConsole = QtWidgets.QAction(MainWindow)
        self.actionRunConsole.setObjectName("actionRunConsole")
        self.actionOpen_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.actionOpen_Directory)
        self.menuFile.addAction(self.actionRecent)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionCloseTab)
        self.menuFile.addAction(self.actionCloseAllTab)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionIndent)
        self.menuEdit.addAction(self.actionUnIndent)
        self.menuEdit.addAction(self.actionLineCut)
        self.menuEdit.addAction(self.actionLineCopy)
        self.menuEdit.addAction(self.actionLinePaste)
        self.menuEdit.addAction(self.actionLineTranspose)
        self.menuEdit.addAction(self.actionLineDuplicate)
        self.menuEdit.addAction(self.actionCommentUncomment)
        self.menuEdit.addAction(self.actionLineUp)
        self.menuEdit.addAction(self.actionLineDown)
        self.menuEdit.addAction(self.actionFoldAll)
        self.menuEdit.addAction(self.actionCurrentFold)
        self.menuEdit.addAction(self.actionUnFold)
        self.menuFind.addAction(self.actionFind)
        self.menuFind.addAction(self.actionFindAll)
        self.menuFind.addAction(self.actionReplace)
        self.menuFind.addAction(self.actionReplaceAll)
        self.menuFind.addAction(self.actionGotoLine)
        self.menuFind.addAction(self.actionHighlight)
        self.menuFind.addAction(self.actionUpperCase)
        self.menuFind.addAction(self.actionLowerCase)
        self.menuFind.addAction(self.actionCamelCase)
        self.menuWindow.addAction(self.actionPythonConsole)
        self.menuWindow.addAction(self.actionRunConsole)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuFind.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.findForwardButton.setText(_translate("MainWindow", "Find"))
        self.findPrevButton.setText(_translate("MainWindow", "Find Prev"))
        self.replaceButton.setText(_translate("MainWindow", "Replace"))
        self.replaceAllButton.setText(_translate("MainWindow", "Replace All"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuFind.setTitle(_translate("MainWindow", "Find"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.actionNew.setText(_translate("MainWindow", "  New                Ctrl+N"))
        self.actionOpen_Directory.setText(_translate("MainWindow", "  Open Directory"))
        self.actionExit.setText(_translate("MainWindow", "Exit                  Alt+F4"))
        self.actionCloseTab.setText(_translate("MainWindow", "Close Tab        Ctrl+W"))
        self.actionCloseAllTab.setText(_translate("MainWindow", "Close All Tab"))
        self.actionSave.setText(_translate("MainWindow", "  Save                Ctrl+S"))
        self.actionSaveAs.setText(_translate("MainWindow", "Save As"))
        self.actionRecent.setText(_translate("MainWindow", "Recent"))
        self.actionCut.setText(_translate("MainWindow", "  Cut                  Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "  Copy               Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "  Paste               Ctrl+V"))
        self.actionUndo.setText(_translate("MainWindow", "  Undo              Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "  Redo               Ctrl+Y"))
        self.actionIndent.setText(_translate("MainWindow", "  Indent             Tab"))
        self.actionUnIndent.setText(_translate("MainWindow", "  UnIndent        Shift+Tab"))
        self.actionUndo.setIcon(QtGui.QIcon("icons/undo.png"))
        self.actionRedo.setIcon(QtGui.QIcon("icons/redo.png"))
        self.actionIndent.setIcon(QtGui.QIcon("icons/indent.png"))
        self.actionUnIndent.setIcon(QtGui.QIcon("icons/dedent.png"))
        self.actionLineCut.setText(_translate("MainWindow", "Line Cut          Ctrl+L"))
        self.actionLineCopy.setText(_translate("MainWindow", "Line Copy       Ctrl+Shift+T"))
        self.actionLinePaste.setText(_translate("MainWindow", "Line Paste       Ctrl+Shift+L"))
        self.actionLineDuplicate.setText(_translate("MainWindow", "Line Duplicate       Ctrl+D"))
        self.actionLineTranspose.setText(_translate("MainWindow", "Line Transpose      Ctrl+T"))
        self.actionCommentUncomment.setText(_translate("MainWindow", "Comment/Uncomment    Alt+/"))
        self.actionGotoLine.setText(_translate("MainWindow", "Goto Line        Ctrl+G"))
        self.actionHighlight.setText(_translate("MainWindow", "  Highlight        Ctrl+M"))
        self.actionUpperCase.setText(_translate("MainWindow", "UpperCase       Alt+U"))
        self.actionLowerCase.setText(_translate("MainWindow", "LowerCase      Alt+L"))
        self.actionCamelCase.setText(_translate("MainWindow", "CamelCase     Alt+C"))
        self.actionFind.setText(_translate("MainWindow", "Find             Ctrl+F"))
        self.actionFindAll.setText(_translate("MainWindow", "Find All     Ctrl+Shift+F"))
        self.actionReplace.setText(_translate("MainWindow", "Replace        Ctrl+R"))
        self.actionReplaceAll.setText(_translate("MainWindow", "Replace All      Ctrl+Shift+R"))
        self.actionLineUp.setText(_translate("MainWindow", "Line Up          Ctrl+Shift+U"))
        self.actionLineDown.setText(_translate("MainWindow", "Line Down     Ctrl+Shift+D"))
        self.actionFoldAll.setText(_translate("MainWindow", "Fold All          Alt+F"))
        self.actionCurrentFold.setText(_translate("MainWindow", "Current Fold  Alt+C"))
        self.actionUnFold.setText(_translate("MainWindow", "UnFold          Alt+Z"))
        self.actionPythonConsole.setText(_translate("MainWindow", "Python Console"))
        self.actionRunConsole.setText(_translate("MainWindow", "Run Console"))
        self.actionOpen_File.setText(_translate("MainWindow", "  Open File        Ctrl+O"))

from _widgets.directory.directoryTree import DirectoryTree
from _widgets.interpreter.interpreterWidget import InterpreterWidget
from _widgets.editor.scintillaEditor import CustomEditorTab, EditorWidget
from _widgets.editor.editorHelper import PythonModuleInfo
