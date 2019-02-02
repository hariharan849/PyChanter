import os as _os
import itertools as _itertools
from PyQt5 import (
    QtGui as _QtGui,
    QtCore as _QtCore,
    QtWidgets as _QtWidgets
)
from launchApplicationUI import Ui_MainWindow
from widgets import EditorWidget
from resources.ui import inputDialog


class MainApplication(_QtWidgets.QMainWindow, Ui_MainWindow):
    nextFileCount = _itertools.count(0, 1)
    recentDirectory = ""
    recentFiles = []
    def __init__(self, parent=None):
        super(MainApplication, self).__init__(parent)
        self.setupUi(self)
        self.findReplaceWidget.setVisible(False)
        self.dialog = None
        self.__setUpActionMenus()
        self._connectWidgets()
        self.__createNewEditor()
        self.showMaximized()

    def _connectWidgets(self):
        self.findButton.clicked.connect(self.__find)
        self.findAllButton.clicked.connect(self.__findAll)
        self.replaceButton.clicked.connect(self.__replace)
        self.replaceAllButton.clicked.connect(self.__replaceAll)
        self.treeView.doubleClicked.connect(self.__createFileTab)

    def __setUpActionMenus(self):
        '''
        Sets up action slot connection for the application
        '''
        self.actionNew_Ctrl_N.triggered.connect(self.__createNewEditor)
        newFile = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+n"), self)
        newFile.activated.connect(self.__createNewEditor)

        self.actionOpen_Directory.triggered.connect(self.__openDirectory)

        self.actionOpen_Ctrl_O.triggered.connect(self.__openFileDialog)
        openFile = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+o"), self)
        openFile.activated.connect(self.__openFileDialog)

        self.actionSave_Ctrl_S.triggered.connect(self.__saveFile)
        saveFile = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+s"), self)
        saveFile.activated.connect(self.__saveFile)

        self.actionSave_As.triggered.connect(self.__saveFileAs)

        self.actionClose_Tab_Ctrl_W.triggered.connect(self.__closeCurrentTab)
        closeTabAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+w"), self)
        closeTabAction.activated.connect(self.__closeCurrentTab)

        self.actionClose_All_Tab.triggered.connect(self.__closeAllTabs)

        self.actionExit_Alt_F4.triggered.connect(self.__safeExit)
        exitAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+f4"), self)
        exitAction.activated.connect(self.__safeExit)

        self.actionCut_Ctrl_X.triggered.connect(self.__cut)
        cutAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+x"), self)
        cutAction.activated.connect(self.__cut)

        self.actionCopy_Ctrl_C.triggered.connect(self.__copy)
        copyAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+c"), self)
        copyAction.activated.connect(self.__copy)

        self.actionPaste_Ctrl_V.triggered.connect(self.__paste)
        pasteAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+v"), self)
        pasteAction.activated.connect(self.__paste)

        self.actionComment_Uncomment_Ctrl.triggered.connect(self.__commentUncomment)
        toggleCommentAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+/"), self)
        toggleCommentAction.activated.connect(self.__commentUncomment)

        self.actionGoto_Line_Ctrl_G.triggered.connect(self.__gotoLine)
        gotoLineAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+g"), self)
        gotoLineAction.activated.connect(self.__gotoLine)

        self.actionHighlight_Ctrl_M.triggered.connect(self.__highLight)
        highlightAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+M"), self)
        highlightAction.activated.connect(self.__highLight)

        self.actionUpperCase_Alt_U.triggered.connect(lambda: self.__convertCase('u'))
        upperCaseAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+u"), self)
        upperCaseAction.activated.connect(lambda: self.__convertCase(True))

        self.actionLowerCase_Alt_L.triggered.connect(lambda: self.__convertCase('l'))
        lowerCaseAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+l"), self)
        lowerCaseAction.activated.connect(lambda: self.__convertCase('l'))

        self.actionCamelCase_Alt_C.triggered.connect(lambda: self.__convertCase('c'))
        camelCaseAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("alt+c"), self)
        camelCaseAction.activated.connect(lambda: self.__convertCase('c'))

        self.actionFind.triggered.connect(self.__findReplace)
        findAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+f"), self)
        findAction.activated.connect(self.__findReplace)

        self.actionFind_All_Ctrl_Shift_F.triggered.connect(self.__findReplace)
        findAllAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+shift+f"), self)
        findAllAction.activated.connect(self.__findReplace)

        self.actionReplace_Ctrl_R.triggered.connect(self.__findReplace)
        replaceAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+r"), self)
        replaceAction.activated.connect(self.__findReplace)

        self.actionReplace_All_Ctrl_Shift_R.triggered.connect(self.__findReplace)
        replaceAllAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+shift+r"), self)
        replaceAllAction.activated.connect(self.__findReplace)

        self.actionLine_Move_Ctrl_Shift_up_down.triggered.connect(self.__lineUp)
        lineUpAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+shift+u"), self)
        lineUpAction.activated.connect(self.__lineUp)

        self.actionLine_Down_Ctrl_Shift_d.triggered.connect(self.__lineDown)
        lineDownAction = _QtWidgets.QShortcut(_QtGui.QKeySequence("ctrl+shift+d"), self)
        lineDownAction.activated.connect(self.__lineDown)

        self.actionFold_All.triggered.connect(self.__foldAll)

    def __createNewEditor(self):
        tabName = "untitled_{0}".format(str(next(self.nextFileCount)))
        editor = EditorWidget()
        newIndex = self.tabWidget.addTab(editor, _os.path.basename(tabName))
        editor.textChanged.connect(self.tabWidget.textChangedSlot)
        self.tabWidget.setCurrentIndex(newIndex)
        editor.setFocus()

    def __openDirectory(self):
        directory = _QtWidgets.QFileDialog.getExistingDirectory(
                    self,
                    "Open a folder",
                    "",
                    _QtWidgets.QFileDialog.ShowDirsOnly
                )
        if not directory:
            return
        self.treeView.displayDirectory(directory)

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
                tabName = tabName[0]
            editor = EditorWidget(filePath=tabName)
            editor.textChanged.connect(self.tabWidget.textChangedSlot)

            newIndex = self.tabWidget.addTab(editor, _os.path.basename(tabName))
            # self.recentFiles.append(tabName)
        except:
            message = "Unexpected error occured while opening file!"
            _QtWidgets.QMessageBox.warning(self, 'Warning', message, buttons=_QtWidgets.QMessageBox.Ok)
            return
        self.tabWidget.setCurrentIndex(newIndex)
        editor.setFocus()
        self.recentDirectory = _os.path.dirname(tabName)

    def __saveFile(self):
        encoding = 'utf-8'
        if not isinstance(self.tabWidget.currentWidget(), EditorWidget):
            return
        editor = self.tabWidget.currentWidget()
        if "untitled" in self.tabWidget.tabText(self.tabWidget.currentIndex()):
            filePath = _QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Save File",
                self.recentDirectory,
                "All Files(*)"
            )
            self.recentDirectory = _os.path.dirname(filePath)
        else:
            filePath = editor.filePath
        text = editor.text()
        try:
            with open(filePath, "w", newline="", encoding=encoding) as file:
                #Write text to the file
                file.write(text)
                #Close the file handle
                file.close()
            self.tabWidget.setTabText(self.tabWidget.currentIndex(),_os.path.basename(filePath))
            editor.isEdited = False
        except Exception as ex:
            print (ex)

    def __saveFileAs(self):
        encoding = 'utf-8'
        if not isinstance(self.tabWidget.currentWidget(), EditorWidget):
            return
        editor = self.tabWidget.currentWidget()
        filePath = _QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save File",
            self.recentDirectory,
            "All Files(*)"
        )
        text = editor.text()
        try:
            with open(filePath, "w", newline="", encoding=encoding) as file:
                # Write text to the file
                file.write(text)
                # Close the file handle
                file.close()
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), _os.path.basename(filePath))
            self.recentDirectory = _os.path.dirname(filePath)
            editor.isEdited = False
        except Exception as ex:
            print (ex)

    def __closeAllTabs(self):
        for count in range(self.tabWidget.count()):
            if isinstance(self.tabWidget.widget(count), EditorWidget) and self.tabWidget.widget(count).isEdited:
                reply = _QtWidgets.QMessageBox.critical(
                    self,
                    'Critical',
                    "You have modified documents!\nAre You sure to close",
                    buttons=_QtWidgets.QMessageBox.Ok|_QtWidgets.QMessageBox.Cancel)
                if reply == _QtWidgets.QMessageBox.Cancel:
                    return
        for count in range(self.tabWidget.count()):
            self.tabWidget.removeTab(count)

    def __closeCurrentTab(self):
        if isinstance(self.tabWidget.currentWidget(), EditorWidget) and self.tabWidget.currentWidget().isEdited:
            reply = _QtWidgets.QMessageBox.critical(
                self,
                'Critical',
                "You have modified documents!\nAre You sure to close",
                buttons=_QtWidgets.QMessageBox.Ok | _QtWidgets.QMessageBox.Cancel)
            if reply == _QtWidgets.QMessageBox.Cancel:
                return
            else:
                self.tabWidget.removeTab(self.tabWidget.currentIndex())

    def __safeExit(self):
        for count in range(self.tabWidget.count()):
            if isinstance(self.tabWidget.widget(count), EditorWidget) and self.tabWidget.widget(count).isEdited:
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

    def __lineUp(self):
        try:
            editor = self.__getFocusedEditor()
            if editor:
                editor.moveLineUp()
        except Exception as ex:
            print (ex.message)

    def __lineDown(self):
        try:
            editor = self.__getFocusedEditor()
            if editor:
                editor.moveLineDown()
        except Exception as ex:
            print (ex.message)

    def __foldAll(self):
        try:
            editor = self.__getFocusedEditor()
            if editor:
                editor.foldAll()
        except Exception as ex:
            print (ex.message)

    def __getFocusedEditor(self):
        for i in range(self.tabWidget.count()):
            if isinstance(self.tabWidget.widget(i), EditorWidget) and self.tabWidget.widget(i).hasFocus():
                return self.tabWidget.widget(i)
        return None

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
            print (editor, self.tabWidget.currentWidget())
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

    def __gotoLine(self):
        editor = self.__getFocusedEditor()
        if editor:
            self.dialog = inputDialog.InputDialog("Enter Line No", self)
            self.dialog.lineValue.setValidator(_QtGui.QIntValidator())
            self.dialog.exec_()
            editor.gotoLine(int(self.dialog.lineValue.text()))

    def __highLight(self):
        editor = self.__getFocusedEditor()
        if editor:
            self.dialog = inputDialog.InputDialog("Enter text to highlight", self)
            self.dialog.exec_()
            editor.highlightText(self.dialog.lineValue.text())

    def __convertCase(self, caseType='l'):
        editor = self.__getFocusedEditor()
        if editor:
            try:
                editor.convertCase(caseType)
            except Exception as ex:
                print (ex)

    def __findReplace(self):
        self.findReplaceWidget.setVisible(True)

    def __find(self):
        # editor = self.__getFocusedEditor()
        editor = self.tabWidget.widget(1)
        if editor:
            try:
                editor.find(self.findValue.text())
            except Exception as ex:
                print (ex)

    def __findAll(self):
        editor = self.__getFocusedEditor()
        if editor:
            try:
                editor.find(self.findValue.text(), findAll=True)
            except Exception as ex:
                print (ex)

    def __replace(self):
        editor = self.__getFocusedEditor()
        editor = self.tabWidget.widget(1)
        if editor:
            try:
                editor.replace(
                    self.findValue.text(),
                    self.replaceValue.text()
                )
            except Exception as ex:
                print (ex)

    def __replaceAll(self):
        # editor = self.__getFocusedEditor()
        editor = self.tabWidget.widget(1)
        if editor:
            try:
                editor.replace(
                    self.findValue.text(),
                    self.replaceValue.text(),
                    replaceAll=True
                )
            except Exception as ex:
                print (ex)

    def __createFileTab(self, index):
        item = self.treeView.model().itemFromIndex(index)
        if not _os.path.isfile(item.fullPath):
            return
        editor = EditorWidget(filePath=item.fullPath)
        newIndex = self.tabWidget.addTab(editor, _os.path.basename(item.fullPath))
        editor.textChanged.connect(self.tabWidget.textChangedSlot)
        self.tabWidget.setCurrentIndex(newIndex)
        editor.setFocus()
        # item = self.treeView.model().item(index)
        # print (item.data())

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
        print (ex)
    sys.exit(app.exec_())