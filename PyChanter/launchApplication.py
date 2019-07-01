import os as _os
import itertools as _itertools
from PyQt5 import (
    QtWidgets as _QtWidgets,
    QtGui as _QtGui,
    QtCore as _QtCore
)
from launchApplicationUI import Ui_MainWindow
from widgets import CustomEditorTab, EditorWidget, InputDialog, DirectoryTree, FindAllDialog, AutoCompleter

class MainApplication(_QtWidgets.QMainWindow, Ui_MainWindow):
    # nextFileCount = _itertools.count(0, 1)
    nextFileCount = -1
    recentDirectory = ""
    recentFiles = []
    def __init__(self, parent=None):
        super(MainApplication, self).__init__(parent)
        self.setupUi(self)
        completerThread = AutoCompleter()
        completerThread.start()
        self.findReplaceWidget.setVisible(False)
        self.directoryTreeDockWidget.setVisible(False)
        self.interpreterDockWidget.setVisible(False)
        self.moduleTreeDockWidget.setVisible(False)
        self.dialog = None
        self._setUpActionMenus()
        self._connectWidgets()
        self.__createNewEditor()
        self.showMaximized()

    def _connectWidgets(self):
        """
        Connect Widgets
        """
        self.editorTabWidget.tabCloseRequested.connect(self.__closeCurrentTab)
        self.findForwardButton.clicked.connect(self.__find)
        self.findPrevButton.clicked.connect(lambda: self.__find(previous=True))
        self.replaceButton.clicked.connect(self.__replace)
        self.replaceAllButton.clicked.connect(self.__replaceAll)

    def _setUpActionMenus(self):
        """
        Sets up action slot connection for the application
        """
        self.actionNew.triggered.connect(self.__createNewEditor)
        newFile = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+n"), self)
        newFile.activated.connect(self.__createNewEditor)

        self.actionOpen_File.triggered.connect(self.__openFileDialog)
        openFile = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+o"), self)
        openFile.activated.connect(self.__openFileDialog)

        self.actionOpen_Directory.triggered.connect(self.__openDirectoryDialog)
        # openFile = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+o"), self)
        # openFile.activated.connect(self.__openFileDialog)

        self.actionSave.triggered.connect(self.__saveFile)
        saveFile = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+s"), self)
        saveFile.activated.connect(self.__saveFile)

        self.actionSaveAs.triggered.connect(self.__saveFileAs)

        self.actionCloseTab.triggered.connect(self.__closeCurrentTab)
        closeTabAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+w"), self)
        closeTabAction.activated.connect(self.__closeCurrentTab)

        self.actionCloseAllTab.triggered.connect(self.__closeAllTabs)

        self.actionExit.triggered.connect(self.__safeExit)
        exitAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+f4"), self)
        exitAction.activated.connect(self.__safeExit)

        self.actionCut.triggered.connect(self.__cut)
        cutAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+x"), self)
        cutAction.activated.connect(self.__cut)

        self.actionCopy.triggered.connect(self.__copy)
        copyAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+c"), self)
        copyAction.activated.connect(self.__copy)

        self.actionPaste.triggered.connect(self.__paste)
        pasteAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+v"), self)
        pasteAction.activated.connect(self.__paste)

        self.actionCommentUncomment.triggered.connect(self.__commentUncomment)
        toggleCommentAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+/"), self)
        toggleCommentAction.activated.connect(self.__commentUncomment)

        self.actionLineUp.triggered.connect(self.__moveEditorLineUp)
        moveLineUpAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+shift+up"), self)
        moveLineUpAction.activated.connect(self.__moveEditorLineUp)

        self.actionLineDown.triggered.connect(self.__moveEditorLineDown)
        moveLineDownAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+shift+down"), self)
        moveLineDownAction.activated.connect(self.__moveEditorLineDown)

        self.actionGotoLine.triggered.connect(self.__gotoLine)
        gotoLineAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+g"), self)
        gotoLineAction.activated.connect(self.__gotoLine)

        self.actionHighlight.triggered.connect(self.__highLight)
        highlightAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+m"), self)
        highlightAction.activated.connect(self.__highLight)

        self.actionUpperCase.triggered.connect(lambda: self.__convertCase('u'))
        upperCaseAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+u"), self)
        upperCaseAction.activated.connect(lambda: self.__convertCase(True))

        self.actionLowerCase.triggered.connect(lambda: self.__convertCase('l'))
        lowerCaseAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+l"), self)
        lowerCaseAction.activated.connect(lambda: self.__convertCase('l'))

        self.actionCamelCase.triggered.connect(lambda: self.__convertCase('c'))
        camelCaseAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+c"), self)
        camelCaseAction.activated.connect(lambda: self.__convertCase('c'))

        self.actionFind.triggered.connect(self.__enableFindReplaceWidget)
        findAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+f"), self)
        findAction.activated.connect(self.__enableFindReplaceWidget)

        self.actionReplace.triggered.connect(self.__enableFindReplaceWidget)
        replaceAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+r"), self)
        replaceAction.activated.connect(lambda: self.__enableFindReplaceWidget(isReplace=True))

        self.actionPythonConsole.triggered.connect(self.__launchInterpreter)
        self.actionRunConsole.triggered.connect(self.__runFile)

        findAllAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+shift+f"), self)
        findAllAction.activated.connect(self.__findAll)

        autoCompleteAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+space"), self)
        autoCompleteAction.activated.connect(self.__triggerAutoComplete)

    def __createNewEditor(self):
        tabName = "untitled_{0}".format(str(self.nextFileCount+1))
        editor = EditorWidget()
        print (dir(editor))
        newIndex = self.editorTabWidget.addTab(editor, _os.path.basename(tabName))
        editor.textChanged.connect(self.editorTabWidget.textChangedSlot)
        self.editorTabWidget.setCurrentIndex(newIndex)
        editor.setFocus()
        self.nextFileCount += 1

    def __openDirectoryDialog(self):
        directory = _QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            self.recentDirectory
        )
        if not directory:
            return
        try:
            self.directoryTreeView.displayDirectory(directory)
            self.directoryTreeDockWidget.setVisible(True)

        except Exception as ex:
            message = "Unexpected error occured while opening file! {0}".format(ex)
            _QtWidgets.QMessageBox.warning(self, 'Warning', message, buttons=_QtWidgets.QMessageBox.Ok)
            return


    def __openFileDialog(self):
        files = _QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Open File",
            self.recentDirectory
        )
        if not files:
            return
        tabName = files[0]
        try:
            if isinstance(tabName, list):
                if not tabName:
                    return
                tabName = tabName[0]
            editor = EditorWidget(filePath=tabName)
            editor.textChanged.connect(self.editorTabWidget.textChangedSlot)

            newIndex = self.editorTabWidget.addTab(editor, _os.path.basename(tabName))
            # self.recentFiles.append(tabName)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            message = "Unexpected error occured while opening file! {0}".format(ex.message)
            _QtWidgets.QMessageBox.warning(self, 'Warning', message, buttons=_QtWidgets.QMessageBox.Ok)
            return
        self.editorTabWidget.setCurrentIndex(newIndex)
        editor.setFocus()
        self.recentDirectory = _os.path.dirname(tabName)

        self.moduleTreeDockWidget.setVisible(True)
        self.moduleTreeView.createModuleTree(editor.text())
        self.moduleTreeView.doubleClicked.connect(editor.moduleInfoClicked)

    def __saveFile(self):
        encoding = 'utf-8'
        if not isinstance(self.editorTabWidget.currentWidget(), EditorWidget):
            return
        editor = self.editorTabWidget.currentWidget()
        if "untitled" in self.editorTabWidget.tabText(self.editorTabWidget.currentIndex()):
            filePath = _QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Save File",
                self.recentDirectory,
                "All Files(*)"
            )
            filePath = filePath[0]
            if not filePath:
                return
            self.recentDirectory = _os.path.dirname(filePath)
            editor.filePath = filePath
        else:
            filePath = editor.filePath
        text = editor.text()
        try:
            with open(filePath, "w", newline="", encoding=encoding) as file:
                #Write text to the file
                file.write(text)
                #Close the file handle
                file.close()
            self.editorTabWidget.setTabText(self.editorTabWidget.currentIndex(), _os.path.basename(filePath))
            editor.isEdited = False
        except Exception as ex:
            print (ex)

    def __saveFileAs(self):
        encoding = 'utf-8'
        if not isinstance(self.editorTabWidget.currentWidget(), EditorWidget):
            return
        editor = self.editorTabWidget.currentWidget()
        filePath = _QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File",
            self.recentDirectory,
            "All Files(*)"
        )
        filePath = filePath[0]
        if not filePath:
            return
        text = editor.text()
        try:
            with open(filePath, "w", newline="", encoding=encoding) as file:
                # Write text to the file
                file.write(text)
                # Close the file handle
                file.close()
            self.editorTabWidget.setTabText(self.editorTabWidget.currentIndex(), _os.path.basename(filePath))
            self.recentDirectory = _os.path.dirname(filePath)
            editor.isEdited = False
        except Exception as ex:
            print (ex)

    def __closeAllTabs(self):
        for count in range(self.editorTabWidget.count()):
            if isinstance(self.editorTabWidget.widget(count), EditorWidget) and self.editorTabWidget.widget(count).isEdited:
                reply = _QtWidgets.QMessageBox.critical(
                    self,
                    'Critical',
                    "You have modified documents!\nAre You sure to close",
                    buttons=_QtWidgets.QMessageBox.Ok|_QtWidgets.QMessageBox.Cancel)
                if reply == _QtWidgets.QMessageBox.Cancel:
                    return
        for count in range(self.editorTabWidget.count()):
            self.editorTabWidget.removeTab(count)
        self.nextFileCount = -1

    def __closeCurrentTab(self):
        if isinstance(self.editorTabWidget.currentWidget(), EditorWidget) and self.editorTabWidget.currentWidget().isEdited:
            reply = _QtWidgets.QMessageBox.critical(
                self,
                'Critical',
                "You have modified documents!\nAre You sure to close",
                buttons=_QtWidgets.QMessageBox.Ok | _QtWidgets.QMessageBox.Cancel)
            if reply == _QtWidgets.QMessageBox.Cancel:
                return
        self.editorTabWidget.removeTab(self.editorTabWidget.currentIndex())
        self.nextFileCount -= 1

    def __safeExit(self):
        for count in range(self.editorTabWidget.count()):
            if isinstance(self.editorTabWidget.widget(count), EditorWidget) and self.editorTabWidget.widget(count).isEdited:
                reply = _QtWidgets.QMessageBox.critical(
                    self,
                    'Critical',
                    "You have modified documents!\nAre You sure to close",
                    buttons=_QtWidgets.QMessageBox.Ok|_QtWidgets.QMessageBox.Cancel)
                if reply == _QtWidgets.QMessageBox.Cancel:
                    return
                else:
                    self.close()

    def __cut(self):
        try:
            editor = self.__getFocusedEditor()
            if editor:
                editor.cut()
        except Exception as ex:
            print (ex.message)

    def __getFocusedEditor(self):
        for i in range(self.editorTabWidget.count()):
            if isinstance(self.editorTabWidget.widget(i), EditorWidget) and self.editorTabWidget.widget(i).hasFocus():
                return self.editorTabWidget.widget(i)
        return self.editorTabWidget.widget(i)

    def __copy(self):
        try:
            editor = self.__getFocusedEditor()
            if editor:
                editor.copy()
        except Exception as ex:
            print (ex.message)

    def __paste(self):
        try:
            editor = self.__getFocusedEditor()
            print (editor, self.editorTabWidget.currentWidget())
            if editor:
                editor.paste()
        except Exception as ex:
            print (ex.message)

    def __commentUncomment(self):
        editor = self.__getFocusedEditor()
        if editor:
            selection = editor.getSelection()
            if selection == (-1, -1, -1, -1) or selection[0] == selection[2]:
                lineNumber = editor.getCursorPosition()[0] + 1
                editor.togglecommentLine(lineNumber)
            else:
                startLineNumber = editor.getSelection()[0] + 1
                endLineNumber = editor.getSelection()[2] + 1
                # Choose un/commenting according to the first line in selection
                editor.togglecommentLines(startLineNumber, endLineNumber)

    def __moveEditorLineDown(self):
        editor = self.__getFocusedEditor()
        if editor:
            editor.moveLineDown()

    def __moveEditorLineUp(self):
        editor = self.__getFocusedEditor()
        if editor:
            editor.moveLineUp()

    def __gotoLine(self):
        editor = self.__getFocusedEditor()
        if editor:
            self.dialog = InputDialog(title='Enter Line No', parent=self)
            result = self.dialog.exec_()
            if not result:
                return
            lineNumber = int(self.dialog.lineValue.text())
            lineText = editor.getLineText(lineNumber)
            editor.setSelection(lineNumber-1, 0, lineNumber-1, len(lineText))

    def __highLight(self):
        editor = self.__getFocusedEditor()
        if editor:
            editor.highlightText(editor.selectedText())

    def __convertCase(self, caseType='l'):
        editor = self.__getFocusedEditor()
        if editor:
            try:
                editor.convertCase(caseType)
            except Exception as ex:
                print (ex)

    def __enableFindReplaceWidget(self, isReplace=False):
        self.findReplaceWidget.setVisible(True)
        editor = self.__getFocusedEditor()
        if editor:
            self.findValue.setText(editor.selectedText())
        self.replaceValue.setVisible(isReplace)
        self.replaceButton.setVisible(isReplace)
        self.replaceAllButton.setVisible(isReplace)

    def __find(self, previous=False):
        editor = self.__getFocusedEditor()
        if editor:
            try:
                editor.find(self.findValue.text(), searchForward=not previous)
            except Exception as ex:
                print (ex)

    def __findAll(self):
        dialog = FindAllDialog(title="Find All", parent=self)
        dialog.exec_()
        directory = dialog.lineValue.text()
        if not directory:
            return


    def __replace(self):
        editor = self.__getFocusedEditor()
        editor = self.editorTabWidget.widget(1)
        if editor:
            try:
                editor.replace(
                    self.findValue.text(),
                    self.replaceValue.text()
                )
            except Exception as ex:
                print (ex)

    def __replaceAll(self):
        editor = self.__getFocusedEditor()
        if editor:
            try:
                editor.replace(
                    self.findValue.text(),
                    self.replaceValue.text(),
                    replaceAll=True
                )
            except Exception as ex:
                print (ex)

    def __launchInterpreter(self):
        self.interpreterDockWidget.setVisible(True)
        self.interpreterWidget.show()

    def __runFile(self):
        self.interpreterDockWidget.setVisible(True)
        self.interpreterWidget.show()
        editor = self.__getFocusedEditor()
        if editor:
            self.interpreterWidget.runFile(editor.filePath)

    def __triggerAutoComplete(self):
        editor = self.__getFocusedEditor()
        if editor:
            editor.triggerAutoComplete()

    def keyPressEvent(self, ev):
        if ev.key() == _QtCore.Qt.Key_Escape and self.dialog:
            self.dialog.close()
            self.dialog.setParent(None)
            self.dialog.deleteLater()
            self.dialog = None
        super(MainApplication, self).keyPressEvent(ev)


if __name__ == '__main__':
    import sys
    app = _QtWidgets.QApplication(sys.argv)
    try:
        console = MainApplication()
        styleFile = _os.path.join(_os.path.dirname(__file__), 'resources', 'styleSheet', 'QTDark.stylesheet')
        with open(styleFile, "r") as fh:
            app.setStyleSheet(fh.read())
        console.show()
    except Exception as ex:
        import traceback

        traceback.print_exc()
        print (ex)
    sys.exit(app.exec_())