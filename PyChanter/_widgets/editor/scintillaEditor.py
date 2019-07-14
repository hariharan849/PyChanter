"""
QScintilla Editor for editing text
"""
import collections as _collections
import itertools as _itertools
import locale as _locale
import os as _os
import re as _re
import jedi as _jedi

from PyChanter import constants as _constants
from PyQt5 import (
    QtCore as _QtCore,
    QtGui as _QtGui,
    Qsci as _Qsci,
    QtWidgets as _QtWidgets,
)
from . import water as _water


class SearchResult(object):
    NOT_FOUND = None
    FOUND = 1
    CYCLED = 2


class CustomEditorTab(_QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        """
        Custom Tab to display Editor Widget
        :param parent:
        """
        super(CustomEditorTab, self).__init__(parent)

    def textChangedSlot(self):
        """
        Custom tab change to change name of tab text
        :return:
        """
        if not self.currentWidget():
            return
        if not isinstance(self.currentWidget(), EditorWidget):
            return
        if self.currentWidget().isEdited:
            return
        self.currentWidget().isEdited = True
        self.setTabText(self.currentIndex(), self.tabText(self.currentIndex()) + "*")


class EditorWidget(_Qsci.QsciScintilla):
    isEdited = False
    HIGHLIGHTINDICATOR = 0
    FIND_INDICATOR = 2
    REPLACE_INDICATOR = 3
    INDICATOR_NUMBER = 5
    searchTextClicked = _QtCore.pyqtSignal(str, int, object)
    gotoDefClicked = _QtCore.pyqtSignal(int, str)
    def __init__(self, parent=None, filePath=None):
        """
        Editor widget based on QsciScintilla
        :param parent:
        :param filePath: FilePath to display text
        """
        super(EditorWidget, self).__init__(parent)

        self._filePath = filePath
        self._findMapping = None
        self._setLexerAndFont()
        self._setFileText(filePath)
        self._setTextWrap()
        self._setEOLMode()
        self._setIndentationSettings()
        self._setCaretSettings()
        self._setMarginSettings()
        self.setBraceMatching(_Qsci.QsciScintilla.SloppyBraceMatch)
        self._setAutocompletionSettings()
        self._connectSignals()
        self.setFolding(self.BoxedTreeFoldStyle)
        self.setTheme(_water)
        self._setStyleSheet()

        self.setContextMenuPolicy(_QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.createCustomContextMenu)

    @property
    def filePath(self):
        return self._filePath

    def setTheme(self, theme):
        """
        Sets theme for editor
        """
        self.setFoldMarginColors(
            theme.FoldMargin.ForeGround,
            theme.FoldMargin.BackGround
        )
        self.setMarginsForegroundColor(theme.LineMargin.ForeGround)
        self.setMarginsBackgroundColor(theme.LineMargin.BackGround)
        self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_STYLESETBACK,
            _Qsci.QsciScintillaBase.STYLE_DEFAULT,
            theme.Paper.Default
        )
        self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_STYLESETBACK,
            _Qsci.QsciScintillaBase.STYLE_LINENUMBER,
            theme.LineMargin.BackGround
        )
        self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_SETCARETFORE,
            theme.Cursor
        )
        self.setCaretLineBackgroundColor(
            theme.Cursor_Line_Background
        )

    def _setStyleSheet(self):
        """
        Set stylesheet for application
        """
        styleFile = _constants.styleSheetFolder
        with open(styleFile, "r") as fh:
            self.setStyleSheet(fh.read())

    def _setLexerAndFont(self):
        """
        Sets Lexer and font for editor widget
        :return:
        """
        self.lexer = _Qsci.QsciLexerPython()
        self.setLexer(self.lexer)
        self.__api = _Qsci.QsciAPIs(self.lexer)

        self.__myFont = _QtGui.QFont()
        self.__myFont.setPointSize(_constants.defaultFontSize)
        self.setFont(self.__myFont)

    def _setFileText(self, filePath):
        """
        Sets text to the editor
        """
        fileData = ""
        if filePath:
            if isinstance(filePath, list):
                fileData = open(filePath[0]).read()
            else:
                fileData = open(filePath).read()
        self.setText(fileData)
        self._filePath = filePath

    def _setTextWrap(self):
        """
        Text wrapping settings
        """
        self.setWrapMode(_Qsci.QsciScintilla.WrapWord)
        self.setWrapVisualFlags(_Qsci.QsciScintilla.WrapFlagByText)
        self.setWrapIndentMode(_Qsci.QsciScintilla.WrapIndentIndented)

    def _setEOLMode(self, flag=False):
        """
        Sets End Of Line visibility
        :param flag(Boolean): Flag to set EOL
        """
        self.setEolMode(_Qsci.QsciScintilla.EolWindows)
        self.setEolVisibility(flag)

    def _setIndentationSettings(self):
        """
        Sets Indentation Settings
        """
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)

    def _setCaretSettings(self):
        """
        Sets Caret Settings
        """
        self.setCaretForegroundColor(_QtGui.QColor("#ff0000ff"))
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(_QtGui.QColor("#1f0000ff"))
        self.setCaretWidth(2)

    def _getmarginFont(self):
        """
        Returns margin font
        """
        font = _QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        return font

    def _setAutocompletionSettings(self):
        """
        Sets AutoCompletions settings
        """
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionReplaceWord(False)
        # self.setAutoCompletionUseSingle(_Qsci.QsciScintilla.AcusAlways)
        self.setAutoCompletionSource(_Qsci.QsciScintilla.AcsAll)

        self.setCallTipsStyle(_Qsci.QsciScintilla.CallTipsNoContext)
        self.setCallTipsVisible(0)
        self.setCallTipsPosition(_Qsci.QsciScintilla.CallTipsBelowText)
        self.setCallTipsBackgroundColor(_QtGui.QColor(0, 255, 0, 80))
        self.setCallTipsForegroundColor(_QtGui.QColor("#ee1111"))
        self.setCallTipsHighlightColor(_QtGui.QColor("#cccccc"))

    def _setMarginSettings(self):
        """
        Sets Margin settings
        """
        font = self._getmarginFont()
        self.setMarginsFont(font)

        # Margin 0 = Symbol margin
        self.setMarginType(0, _Qsci.QsciScintilla.SymbolMargin)
        self.setMarginWidth(0, "00")
        self.markerDefine(_Qsci.QsciScintilla.Circle, 3)
        self.setMarginMarkerMask(1, 0b1111)
        self.setMarkerBackgroundColor(_QtGui.QColor("#ee1111"))

        # Margin 1 = Line number
        self.setMarginType(1, _Qsci.QsciScintilla.NumberMargin)
        fontmetrics = _QtGui.QFontMetrics(font)
        self.setMarginWidth(1, fontmetrics.width("00000") + 6)
        self.setMarginsBackgroundColor(_QtGui.QColor("#cccccc"))
        # Margin mouse clicks
        self.setMarginSensitivity(1, True)

    def _connectSignals(self):
        """
        Widget connections goes here
        """
        self.marginClicked.connect(self.__marginLeftClicked)
        self.marginRightClicked.connect(self.__marginRightClicked)

    def getLineText(self, lineNumber):
        """
        Return the text of the selected line in the scintilla document
        :param lineNumber: int
        :return: str
        """
        lineText = self.text(lineNumber - 1)
        return lineText.replace("\n", "")

    def togglecommentLine(self, lineNumber):
        """
        Toggle comment/uncomment line for the passed line number
        :param lineNumber: int
        """
        lineText = self.getLineText(lineNumber)
        if lineText.startswith('#'):
            lineText = lineText[1:]
        else:
            lineText = '#' + lineText
        self.setSelection(lineNumber-1, 0, lineNumber, 0)
        self.replaceSelectedText(lineText + "\n")
        self.setCursorPosition(lineNumber - 1, 0)

    def togglecommentLines(self, startLineNumber, endLineNumber):
        """
        Toggle comment/uncomment lines for the passed line number
        :param startLineNumber: int
        :param endLineNumber: int
        """
        lineText = self.getLineText(startLineNumber)
        comment = False
        if lineText.startswith('#'):
            comment = True
        for lineNumber in range(startLineNumber, endLineNumber+1):
            lineText = self.getLineText(lineNumber)
            self.setSelection(lineNumber-1, 0, lineNumber, 0)
            if comment:
                self.replaceSelectedText(lineText[1:] + "\n")
            else:
                self.replaceSelectedText('#' + lineText + "\n")
        self.setCursorPosition(endLineNumber-1, 0)

    def _setIndicator(self, indicator, foreColor):
        """
        Set the indicator settings
        """
        self.indicatorDefine(
            _Qsci.QsciScintillaBase.INDIC_ROUNDBOX,
            indicator
        )
        self.setIndicatorForegroundColor(
            foreColor,
            indicator
        )
        self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_SETINDICATORCURRENT,
            indicator
        )

    def moveLineDown(self):
        """
        Moves Line down
        """
        self.SendScintilla(_Qsci.QsciScintilla.SCI_LINECUT)
        self.SendScintilla(_Qsci.QsciScintilla.SCI_LINEDOWN)
        self.SendScintilla(_Qsci.QsciScintilla.SCI_PASTE)
        self.SendScintilla(_Qsci.QsciScintilla.SCI_LINEUP)

    def moveLineUp(self):
        """
        Moves Line up
        """
        self.SendScintilla(_Qsci.QsciScintilla.SCI_LINECUT)
        self.SendScintilla(_Qsci.QsciScintilla.SCI_LINEUP)
        self.SendScintilla(_Qsci.QsciScintilla.SCI_PASTE)
        self.SendScintilla(_Qsci.QsciScintilla.SCI_LINEUP)

    def foldEntireFile(self):
        """
        Folds Whole file
        """
        self.foldAll()

    def clearAllFoldings(self):
        """
        UnFolds Whole file
        """
        self.clearFolds()

    def foldCurrentMethod(self, lineNumber):
        """
        Folds Current method the line number is
        :param lineNumber: int
        """
        self.foldLine(lineNumber)

    def _setIndicatorHighlight(self):
        """
        Sets highlight color
        """
        self._setIndicator(
            self.HIGHLIGHTINDICATOR,
            _QtGui.QColor(0, 255, 0, 80)
        )

    def _indexStringsInText(self, searchText, text, caseSensitive=False, regularExpression=False, textToBytes=False, wholeWords=False):

        # Check if whole words only should be matched
        if wholeWords == True:
            searchText = r"\b(" + searchText + r")\b"
        # Convert text to bytes so that utf-8 characters will be parsed correctly
        if textToBytes == True:
            searchText = bytes(searchText, "utf-8")
            text = bytes(text, "utf-8")
        # Set the search text according to the regular expression selection
        if regularExpression == False:
            searchText = _re.escape(searchText)
        # Compile expression according to case sensitivity flag
        if caseSensitive == True:
            compiledSearchRe = _re.compile(searchText)
        else:
            compiledSearchRe = _re.compile(searchText, _re.IGNORECASE)
        # Create the list with all of the matches
        listOfMatches = [(0, match.start(), 0, match.end()) for match in _re.finditer(compiledSearchRe, text)]
        return listOfMatches

    def findAll(self):
        """
        Show find all
        """
        matches = self._indexStringsInText(
            searchText,
            inputText,
            caseSensitive,
            regularExpression,
            textToBytes,
            wholeWords
        )

    def _findAllFromInputText(self, searchText, inputText, caseSensitive=False, regularExpression=False, textToBytes=False, wholeWords=False):
        """
        Find all instances of a string and return a list of (line, index_start, index_end)
        """
        #Find all instances of the search string and return the list
        matches = self._indexStringsInText(
            searchText,
            inputText,
            caseSensitive,
            regularExpression,
            textToBytes,
            wholeWords
        )
        return matches

    def _highlightRaw(self, highlightList):
        """
        Core highlight function that uses Scintilla messages to style indicators.
        QScintilla's fillIndicatorRange function is to slow for large numbers of
        highlights!
        INFO:   This is done using the scintilla "INDICATORS" described in the official
                scintilla API (http://www.scintilla.org/ScintillaDoc.html#Indicators)
        """
        scintillaCommand = _Qsci.QsciScintillaBase.SCI_INDICATORFILLRANGE
        for highlight in highlightList:
            start = highlight[1]
            length = highlight[3] - highlight[1]
            self.SendScintilla(
                scintillaCommand,
                start,
                length
            )

    def _findText(self, searchText, caseSensitive=False, searchForward=True, regularExpression=False):
        def focusEntireFoundText():
            """
            Nested function for selection the entire found text
            """
            # Save the currently found text selection attributes
            position = self.getSelection()
            # Set the cursor to the beginning of the line, so that in case the
            # found string index is behind the previous cursor index, the whole
            # found text is shown!
            self.setCursorPosition(position[0], 0)
            self.setSelection(position[0], position[1], position[2], position[3])

        # Set focus to the tab that will be searched
        if regularExpression == True:
            # Get the absolute cursor index from line/index position
            line, index = self.getCursorPosition()
            absolutePosition = self.positionFromLineIndex(line, index)
            # Compile the search expression according to the case sensitivity
            if caseSensitive == True:
                compiledSearchRe = _re.compile(searchText)
            else:
                compiledSearchRe = _re.compile(searchText, _re.IGNORECASE)
            # Search based on the search direction
            if searchForward == True:
                # Regex search from the absolute position to the end for the search expression
                searchResult = _re.search(compiledSearchRe, self.text()[absolutePosition:])
                if searchResult != None:
                    #Select the found expression
                    resultStart = absolutePosition + searchResult.start()
                    resultEnd = resultStart + len(searchResult.group(0))
                    self.setCursorPosition(0, resultStart)
                    self.setSelection(0, resultStart, 0, resultEnd)
                    # Return successful find
                    return SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    searchResult = _re.search(compiledSearchRe, self.text())
                    if searchResult != None:
                        # Select the found expression
                        resultStart    = searchResult.start()
                        resultEnd      = resultStart + len(searchResult.group(0))
                        self.setCursorPosition(0, resultStart)
                        self.setSelection(0, resultStart, 0, resultEnd)
                        print("Reached end of document, started from the top again!")
                        # Return cycled find
                        return SearchResult.CYCLED
                    else:
                        print("Text was not found!")
                        return SearchResult.NOT_FOUND
            else:
                # Move the cursor one character back when searching backard
                # to not catch the same search result again
                cursorPosition = self.getAbsoluteCursorPosition()
                searchText = self.text()[:cursorPosition]
                # Regex search from the absolute position to the end for the search expression
                searchResult = [m for m in _re.finditer(compiledSearchRe, searchText)]
                if searchResult != []:
                    #Select the found expression
                    resultStart    = searchResult[-1].start()
                    resultEnd      = searchResult[-1].end()
                    self.setCursorPosition(0, resultStart)
                    self.setSelection(0, resultStart, 0, resultEnd)
                    # Return successful find
                    return SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    searchResult = [m for m in _re.finditer(compiledSearchRe, self.text())]
                    if searchResult != []:
                        # Select the found expression
                        resultStart    = searchResult[-1].start()
                        resultEnd      = searchResult[-1].end()
                        self.setCursorPosition(0, resultStart)
                        self.setSelection(0, resultStart, 0, resultEnd)
                        print("Reached end of document, started from the top again!")
                        # Return cycled find
                        return SearchResult.CYCLED
                    else:
                        print("Text was not found!")
                        return SearchResult.NOT_FOUND
        else:
            # Move the cursor one character back when searching backard
            # to not catch the same search result again
            if searchForward == False:
                line, index = self.getCursorPosition()
                self.setCursorPosition(line, index-1)
            # "findFirst" is the QScintilla function for finding text in a document
            searchResult = self.findFirst(
                searchText,
                False,
                caseSensitive,
                False,
                False,
                forward=searchForward
            )
            if searchResult == False:
                # Try to find text again from the top or at the bottom of
                # the scintilla document, depending on the search direction
                if searchForward == True:
                    sLine = 0
                    sIndex = 0
                else:
                    sLine = len(self.lineList)-1
                    sIndex = len(self.text())
                innerResult = self.findFirst(
                    searchText,
                    False,
                    caseSensitive,
                    False,
                    False,
                    forward=searchForward,
                    line=sLine,
                    index=sIndex
                )
                if innerResult == False:
                    return -1
                else:
                    focusEntireFoundText()
                    # Return cycled find
                    return 2
            else:
                # Found text
                focusEntireFoundText()
                # Return successful find
                return 1

    def gotoLine(self, lineNumber):
        """
        Shows goto line
        :param lineNumber: int
        :return:
        """
        lineText = self.getLineText(lineNumber)
        self.setSelection(lineNumber - 1, 0, lineNumber - 1, len(lineText))

    def highlightText(self, highlightText, caseSensitive=False, regularExpression=False):
        """
        Highlight all instances of the selected text with a selected colour
        :param highlightText: str
        :param caseSensitive: boolean
        :param regularExpression: boolean
        """
        #Setup the indicator style, the highlight indicator will be 0
        self._setIndicatorHighlight()
        #Get all instances of the text using list comprehension and the re module
        matches = self._findAllFromInputText(
            highlightText,
            self.text(),
            caseSensitive=caseSensitive,
            regularExpression=regularExpression,
            textToBytes=True
        )
        #Check if the match list is empty
        if matches:
            #Use the raw highlight function to set the highlight indicators
            self._highlightRaw(matches)
            self._findText(highlightText, caseSensitive, True, regularExpression)
            return matches
        else:
            print ("no Matches")

    def convertCase(self, caseType='l'):
        """
        Toggles case sensitivity on caseType(l or u)
        :param caseType: str
        """
        #Get the start and end point of the selected text
        startLine, startIndex, endLine, endIndex = self.getSelection()
        #Get the currently selected text
        selectedText = self.selectedText()
        #Convert it to the selected case
        if caseType == 'l':
            selectedText = selectedText.lower()
        elif caseType == 'u':
            selectedText = selectedText.upper()
        else:
            splittedText = selectedText.split('_')
            selectedText = splittedText[0] + ''.join(map(lambda x: x.capitalize(), splittedText[1:]))
        #Replace the selection with the new upercase text
        self.replaceSelectedText(selectedText)
        #Reselect the previously selected text
        self.setSelection(startLine, startIndex,  endLine, endIndex)

    def _findAndReplace(self, searchText, replaceText, caseSensitive=False, searchForward=True, regularExpression=False):
        """Find next instance of the search string and replace it with the replace string"""
        if regularExpression == True:
            # Check if expression exists in the document
            searchResult = self._findText(
                searchText, caseSensitive, searchForward, regularExpression
            )
            if searchResult != SearchResult.NOT_FOUND:
                if caseSensitive == True:
                    compiledSearchRe = _re.compile(searchText)
                else:
                    compiledSearchRe = _re.compile(searchText, _re.IGNORECASE)
                # The search expression is already selected from the findText function
                found_expression = self.selectedText()
                # Save the found selected text line/index information
                savedSelection = self.getSelection()
                # Replace the search expression with the replace expression
                replacement = _re.sub(compiledSearchRe, replaceText, found_expression)
                # Replace selected text with replace text
                self.replaceSelectedText(replacement)
                self.setSelection(
                    savedSelection[0],
                    savedSelection[1],
                    savedSelection[2],
                    savedSelection[1] + len(replacement)
                )
                return True
            else:
                # Search text not found
                print("Text was not found!")
                return False
        else:
            # Check if string exists in the document
            searchResult = self._findText(searchText, caseSensitive)
            if searchResult != -1:
                # Save the found selected text line/index information
                savedSelection = self.getSelection()
                # Replace selected text with replace text
                self.replaceSelectedText(replaceText)
                # Select the newly replaced text
                self.setSelection(
                    savedSelection[0],
                    savedSelection[1],
                    savedSelection[2],
                    savedSelection[1] + len(replaceText)
                )
                return True
            else:
                # Search text not found
                print("Text was not found!")
                return False

    def _clearHighlights(self):
        """
        Clear all highlighted text
        """
        # Clear the highlight indicators
        self.clearIndicatorRange(
            0,
            0,
            self.lines(),
            self.lineLength(self.lines() - 1),
            self.HIGHLIGHTINDICATOR
        )
        # Clear the replace indicators
        self.clearIndicatorRange(
            0,
            0,
            self.lines(),
            self.lineLength(self.lines() - 1),
            self.REPLACE_INDICATOR
        )
        # Clear the find indicators
        self.clearIndicatorRange(
            0,
            0,
            self.lines(),
            self.lineLength(self.lines() - 1),
            self.FIND_INDICATOR
        )

    def _setIndicator(self, indicator, foreColor):
        """
        Set the indicator settings
        """
        self.indicatorDefine(
            _Qsci.QsciScintillaBase.INDIC_ROUNDBOX,
            indicator
        )
        self.setIndicatorForegroundColor(
            foreColor,
            indicator
        )
        self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_SETINDICATORCURRENT,
            indicator
        )

    def _setIndicatorReplace(self):
        """
        Set the appearance of the highlight indicator
        """
        self._setIndicator(
            self.REPLACE_INDICATOR,
            QColor(50, 180, 255, 80)
        )

    def _replaceAndIndex(self, inputString, searchText, replaceText, caseSensitive=False, regularExpression=False):
        """
        Function that replaces the search text with replace text in a string,
        using regular expressions if specified, and returns the
        line numbers and indexes of the replacements as a list.
        """
        # First check if the replacement action is needed
        if searchText == replaceText and caseSensitive:
            return None, inputString
        elif searchText.lower() == replaceText.lower() and not caseSensitive:
            return None, inputString
        # Initialize the return variables
        replacedText = None
        # Find the search text matches that will be highlighted (pre-replacement)
        # Only when not searching with regular expressions
        if not regularExpression:
            matches = self._indexStringsInText(
                searchText,
                inputString,
                caseSensitive,
                regularExpression,
                textToBytes=True
            )
            # Create a matches list according to regular expression selection
            # Create a matches list according to regular expression selection
        if regularExpression:
            # Compile the regular expression object according to the case sensitivity
            if caseSensitive:
                compiledSearchRe = _re.compile(searchText)
            else:
                compiledSearchRe = _re.compile(searchText, _re.IGNORECASE)
            # Replace all instances of search text with the replace text
            replacedText = _re.sub(compiledSearchRe, replaceText, inputString)
            replacedMatchIndexes = []
            # Split old and new texts into line lists
            splitInputText = inputString.split("\n")
            splitReplacedText = replacedText.split("\n")
            # Loop through the old text and compare it line-by-line to the old text
            try:
                for i in range(len(splitInputText)):
                    if splitInputText[i] != splitReplacedText[i]:
                        replacedMatchIndexes.append(i)
            except:
                # If regular expression replaced lines,
                # then we cannot highlight the replacements
                replacedMatchIndexes = []
        else:
            replacedText = None
            if caseSensitive:
                # Standard string replace
                replacedText = inputString.replace(searchText, replaceText)
            else:
                # Escape the regex special characters
                newSearchText = _re.escape(searchText)
                # Replace backslashes with double backslashes, so that the
                # regular expression treats backslashes the same as standard
                # Python string replace!
                newReplaceText = replaceText.replace("\\", "\\\\")
                compiledSearchRe = _re.compile(newSearchText, _re.IGNORECASE)
                replacedText = _re.sub(
                    compiledSearchRe,
                    newReplaceText,
                    inputString
                )
            replacedMatchIndexes = []
            # Loop while storing the new indexes
            diff = 0
            blSearch = bytes(searchText, "utf-8")
            blSearch = len(blSearch.replace(b"\\", b" "))
            blReplace = bytes(replaceText, "utf-8")
            blReplace = len(blReplace.replace(b"\\", b" "))
            for i, match in enumerate(matches):
                # Subtract the length of the search text from the match index,
                # to offset the shortening of the whole text when the lenght
                # of the replace text is shorter than the search text
                diff = (blReplace - blSearch) * i
                newIndex = match[1] + diff
                # Check if the index correction went into a negative index
                if newIndex < 0:
                    newIndex = 0
                # The line is always 0, because Scintilla also allows
                # indexing over multiple lines! If the index number goes
                # over the length of a line, it "overflows" into the next line.
                # Basically this means that you can access any line/index by
                # treating the whole text not as a list of lines, but as an array.
                replacedMatchIndexes.append(
                    (
                        0,
                        newIndex,
                        0,
                        newIndex + blReplace
                    )
                )
        # Return the match list and the replaced text
        return replacedMatchIndexes, replacedText

    def _replaceAll(self, searchText, replaceText, caseSensitive=False, regularExpression=False):
        """Replace all occurences of a string in a scintilla document"""
        # Store the current cursor position
        currentPosition = self.getCursorPosition()
        # Move cursor to the top of the document, so all the search string instances will be found
        self.setCursorPosition(0, 0)
        # Clear all previous highlights
        self._clearHighlights()
        # Setup the indicator style, the replace indicator is 1
        self._setIndicatorReplace()
        # Correct the displayed file name
        file_name = self._filePath
        # Check if there are any instances of the search text in the document
        # based on the regular expression flag
        searchResult = None
        if regularExpression == True:
            # Check case sensitivity for regular expression
            if caseSensitive == True:
                compiledSearchRe = _re.compile(searchText)
            else:
                compiledSearchRe = _re.compile(searchText, _re.IGNORECASE)
            searchResult = _re.search(compiledSearchRe, self.text())
        else:
            searchResult = self._findText(searchText, caseSensitive)
        if searchResult == -1:
            message = "No matches were found in '{}'!".format(file_name)
            print(message)
            return
        # Use the re module to replace the text
        text = self.text()
        matches, replacedText = self._replaceAndIndex(
            text,
            searchText,
            replaceText,
            caseSensitive,
            regularExpression,
        )
        # Check if there were any matches or
        # if the search and replace text were equivalent!
        if matches != None:
            # Replace the text
            self._replaceEntireText(replacedText)
            # Matches can only be displayed for non-regex functionality
            if regularExpression == True:
                # Build the list of matches used by the highlightRaw function
                corrected_matches = []
                for i in matches:
                    index = self.positionFromLineIndex(i, 0)
                    corrected_matches.append(
                        (
                            0,
                            index,
                            0,
                            index + len(self.text(i)),
                        )
                    )
                # Display the replacements in the REPL tab
                if len(corrected_matches) < settings.Editor.maximum_highlights:
                    message = "{} replacements:".format(file_name)
                    print (message)
                    for match in corrected_matches:
                        line = self.lineIndexFromPosition(match[1])[0] + 1
                        index = self.lineIndexFromPosition(match[1])[1]
                        message = "    replacement made in line:{:d}".format(line)
                        print (message)
                else:
                    message = "{:d} replacements made in {}!\n".format(
                        len(corrected_matches),
                        file_name
                    )
                    message += "Too many to list individually!"
                    print (message)
                # Highlight and display the line difference between the old and new texts
                self._highlightRaw(corrected_matches)
            else:
                # Display the replacements in the REPL tab
                if len(matches) < settings.Editor.maximum_highlights:
                    message = "{} replacements:".format(file_name)
                    print(message)
                    for match in matches:
                        line = self.lineIndexFromPosition(match[1])[0] + 1
                        index = self.lineIndexFromPosition(match[1])[1]
                        message = "    replaced \"{}\" in line:{:d} column:{:d}".format(
                            searchText,
                            line,
                            index
                        )
                        print(message)
                else:
                    message = "{:d} replacements made in {}!\n".format(
                        len(matches),
                        file_name
                    )
                    message += "Too many to list individually!"
                    print(message)
                # Highlight and display the replaced text
                self._highlightRaw(matches)
            # Restore the previous cursor position
            self.setCursorPosition(currentPosition[0], currentPosition[1])
        else:
            message = "The search string and replace string are equivalent!\n"
            message += "Change the search/replace string or change the case sensitivity!"
            print(message)

    # def replaceInSelection(self, searchText, replaceText, caseSensitive=False, regularExpression=False):
    #     """Replace all occurences of a string in the current selection in the scintilla document"""
    #     # Get the start and end point of the selected text
    #     startLine, startIndex, end_line, end_index = self.getSelection()
    #     # Get the currently selected text and use the re module to replace the text
    #     selected_text = self.selectedText()
    #     replacedText = functions.regex_replaceText(
    #         selected_text,
    #         searchText,
    #         replaceText,
    #         caseSensitive,
    #         regularExpression
    #     )
    #     # Check if any replacements were made
    #     if replacedText != selected_text:
    #         # Put the text back into the selection space and select it again
    #         self.replaceSelectedText(replacedText)
    #         newEndLine = startLine
    #         newEndIndex = startIndex + len(bytearray(replacedText, "utf-8"))
    #         self.setSelection(startLine, startIndex, newEndLine, newEndIndex)
    #     else:
    #         message = "No replacements were made!"
    #         print (message)

    def _replaceEntireText(self, newText):
        """
        Replace the entire text of the document
        """
        # Select the entire text
        self.selectAll(True)
        # Replace the text with the new
        self.replaceSelectedText(newText)

    def find(self, findText, findAll=False, searchForward=True, caseSensitive=False):
        """
        Find the text in the editor
        :param findText: Search text
        :param findAll: Bool to highlight text
        :param searchForward: Bool search the text forward
        :param caseSensitive: Bool case sensitive
        """
        self._findText(findText, searchForward=searchForward, caseSensitive=caseSensitive)

    def replace(self, findText, replaceText, replaceAll=False):
        """
        Replace the text
        :param findText: str to find
        :param replaceText: str to replace
        :param replaceAll: bool falg to replaceAll
        """
        if replaceAll:
            self._replaceAll(findText, replaceText)
        else:
            self._findAndReplace(findText, replaceText)

    def __marginLeftClicked(self, marginNo, lineNo, state):
        """
        Mouse Left Click handler
        :param marginNo: int
        :param lineNo: int
        :param state:
        :return:
        """
        if state == Qt.ControlModifier:
            # Show green dot.
            self.markerAdd(lineNo, 0)

        elif state == Qt.ShiftModifier:
            # Show green arrow.
            self.markerAdd(lineNo, 1)

        elif state == Qt.AltModifier:
            # Show red dot.
            self.markerAdd(lineNo, 2)

        else:
            # Show red arrow.
            if self.markersAtLine(lineNo) == 8:
                self.markerDelete(lineNo, 3)
            else:
                self.markerAdd(lineNo, 3)

    def __marginRightClicked(self, marginNo, line_nr, state):
        pass

    @staticmethod
    def findTextInDirectory(searchText, searchDir, caseSensitive=False):
        """
        Search for the specified text in files in the specified directory and return a file list and
        lines where the text was found at.
        """
        # Check if the directory is valid
        if _os.path.isdir(searchDir) == False:
            return -1
        # Check if searching over multiple lines
        elif '\n' in searchText:
            return -2
        # Create an empty file list
        textFileList = []
        walkTree = _os.walk(searchDir)
        # "walk" through the directory tree and save the readable files to a list
        for root, subFolders, files in walkTree:
            for file in files:
                # Merge the path and filename
                completeFilePath = _os.path.join(root, file)
                if EditorWidget._validateTextFile(completeFilePath) != None:
                    # On windows, the function "_os.path.join(root, file)" line gives a combination of "/" and "\\",
                    # which looks weird but works. The replace was added to have things consistent in the return file list.
                    completeFilePath = completeFilePath.replace("\\", "/")
                    textFileList.append(completeFilePath)
        # Search for the text in found files
        returnFileDict = _collections.defaultdict(list)
        for file in textFileList:
            try:
                fileLines = EditorWidget._readFileToList(file)
                # Set the comparison according to case sensitivity
                if caseSensitive == False:
                    compareSearchText = searchText.lower()
                else:
                    compareSearchText = searchText
                # Check the file line by line
                for i, line in enumerate(fileLines):
                    if caseSensitive == False:
                        line = line.lower()
                    if compareSearchText in line:
                        returnFileDict[file].append({i: fileLines[i]})
            except:
                continue
        # Return the generated list
        return returnFileDict

    @staticmethod
    def _validateTextFile(fileWithPath):
        """Test if a file is a plain text file and can be read"""
        try:
            file = open(fileWithPath, "r", encoding=_locale.getpreferredencoding(), errors="strict")
            # Read only a couple of lines in the file
            for line in _itertools.islice(file, 10):
                line = line
            file.readlines()
            # Close the file handle
            file.close()
            # Return the systems preferred encoding
            return _locale.getpreferredencoding()
        except:
            validencodings = ["utf-8", "ascii", "utf-16", "utf-32", "iso-8859-1", "latin-1"]
            for currentEncoding in validencodings:
                try:
                    file = open(fileWithPath, "r", encoding=currentEncoding, errors="strict")
                    # Read only a couple of lines in the file
                    for line in _itertools.islice(file, 10):
                        line = line
                    # Close the file handle
                    file.close()
                    # Return the succeded encoding
                    return currentEncoding
                except:
                    # Error occured while reading the file, skip to next iteration
                    continue
        # Error, no encoding was correct
        return None

    @staticmethod
    def _readFileToList(filePath):
        """Read contents of a text file to a list"""
        text = EditorWidget._readFileToString(filePath)
        if text != None:
            return text.split("\n")
        else:
            return None

    @staticmethod
    def _readFileToString(filePath):
        """
        Read contents of a text file to a single string
        :param filePath: str
        """
        # Test if a file is in binary format
        binaryText = EditorWidget._testBinaryFile(filePath)
        if binaryText != None:
            return
        else:
            # File is not binary, loop through encodings to find the correct one.
            validEncodings = ["utf-8", "cp1250", "ascii", "utf-16", "utf-32", "iso-8859-1", "latin-1"]
            for currentEncoding in validEncodings:
                try:
                    # If opening the file in the default Ex.Co. encoding fails,
                    # open it using the prefered system encoding!
                    with open(filePath, "r", encoding=currentEncoding, errors="strict") as file:
                        # Read the whole file with "read()"
                        text = file.read()
                        # Close the file handle
                        file.close()
                    # Return the text string
                    return text
                except:
                    # Error occured while reading the file, skip to next encoding
                    continue
        # Error, no encoding was correct
        return None

    @staticmethod
    def _testBinaryFile(filePath):
        """Test if a file is in binary format"""
        file = open(filePath, "rb")
        #Read only a couple of lines in the file
        binaryText = None
        for line in _itertools.islice(file, 20):
            if b"\x00" in line:
                #Return to the beginning of the binary file
                file.seek(0)
                #Read the file in one step
                binaryText = file.read()
                break
        file.close()
        #Return the result
        return binaryText

    def triggerAutoComplete(self):
        """
        Autocompletions for text
        """
        rowNo, colNo = self.getCursorPosition()
        if not colNo:
            return
        script = _jedi.Script(self.text(), rowNo + 1, colNo, self._filePath)
        for ac in script.completions():
            completion = ac.name
            if completion.startswith("_"):
                continue
            self.__api.add(completion)

            signature = script.call_signatures()
            if signature:
                for sig in signature:
                    funcName = sig.full_name
                    funcParams = []
                    for param in sig.params:
                        funcParams.append(param.full_name)
                    self.__api.add("{0}({1})".format(funcName, ", ".join(funcParams)))

        self.__api.prepare()
        self.autoCompleteFromAPIs()

    def moduleInfoClicked(self, item):
        """
        Handles Click from node tree
        """
        lineNumber = item.data().split(":")
        if lineNumber:
            # Parsing String
            lineNumber = lineNumber[-1][:-1]
            self.gotoLine(int(lineNumber))

    def _findAllClick(self, line, index, keys):
        """
        Connect to the indicator signals for feedback when an indicator is clicked or
        a mouse button is released over an indicator
        """
        # Use the low level SendScintilla function to get the indicator's value
        position = self.positionFromLineIndex(line, index)
        # The value can only be set using the low level API described at line 165
        # of this file. Otherwise the value will always be '1'.
        value = self.SendScintilla(
            _Qsci.QsciScintilla.SCI_INDICATORVALUEAT,
            self.INDICATOR_NUMBER,
            position
        )
        textAtLine = self.text(line)
        lineNo = textAtLine.split()[2]

        fileName, lineNo, searchText = self._findMapping[line+1]
        self.searchTextClicked.emit(fileName, lineNo, searchText)

    def setFindMapping(self, findMapping):
        """
        Find Text mapping
        :param findMapping: dict
        """
        self._findMapping = findMapping

    def createHotspot(self, matches, searchText):
        """
        To add a value to an indicator that can later be retrieved by the click or release signals,
        it is necessery to use the low level API to fill the indicator using SendScintilla!
        """
        # Select the indicator
        self.SendScintilla(
            _Qsci.QsciScintilla.SCI_SETINDICATORCURRENT,
            self.INDICATOR_NUMBER
        )
        # Give it a value.
        # This can be used for determinig how to handle the clicked/released indicator signals.
        value = 123
        self.SendScintilla(
            _Qsci.QsciScintilla.SCI_SETINDICATORVALUE,
            value
        )
        # Fill the indicator
        for match in matches:
            _, startPosition, _, endPosition = match
            # fill_line = 4  # This is the 5th line in the document, as the indexes in Python start at 0!
            # start_position = self.positionFromLineIndex(fill_line, 0)
            # length = len(self.text(fill_line))
            self.SendScintilla(
                _Qsci.QsciScintilla.SCI_INDICATORFILLRANGE,
                startPosition,
                endPosition-startPosition
            )

        self.indicatorClicked.connect(self._findAllClick)

    def createCustomContextMenu(self, ev):

        menu = self.createStandardContextMenu()

        gotoDefAction = _QtWidgets.QAction('Goto Definition')
        gotoDefAction.triggered.connect(lambda: self.triggerGotoDefinition(ev))

        menu.addAction(gotoDefAction)
        menu.popup(self.mapToGlobal(ev))
        menu.exec_()

    def _getJediScript(self, ev):
        """
        Returns Script at passed ev
        """
        rowNo = self.lineAt(ev.pos())
        if rowNo == -1:
            return None, None
        hoverWord = self.wordAtPoint(ev.pos())
        colNo = self.text(rowNo).find(hoverWord)
        if colNo == -1:
            return None, None
        return _jedi.Script(self.text(), rowNo + 1, colNo + 1, self._filePath), hoverWord

    def triggerGotoDefinition(self):
        rowNo, colNo = self.getCursorPosition()
        if not colNo:
            return
        script = _jedi.Script(self.text(), rowNo + 1, colNo, self._filePath)
        lineNos, modulePaths = [], []
        for ac in script.goto_assignments():
            lineNos.append(ac.line)
            modulePaths.append(ac.module_path)

        if len(lineNos) > 1:
            pass
        self.gotoDefClicked.emit(lineNos[0], modulePaths[0])

    def mouseMoveEvent(self, ev):
        """
        Handles hovered word docstring
        """
        super(EditorWidget, self).mouseMoveEvent(ev)
        pt = ev.pos()
        script, hoverWord = self._getJediScript(ev)
        if not script:
            return
        docString = ''
        for ac in script.goto_assignments():
            if not ac.docstring():
                return
            if hoverWord == ac.name:
                print (ac.line)
                print (ac.module_path)
                docString = ac.docstring()
                break
        if not docString.strip():
            return
        pos = self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_POSITIONFROMPOINTCLOSE,
            pt.x(),
            pt.y()
        )
        start = self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_WORDSTARTPOSITION,
            pos,
            True
        )
        end = self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_WORDENDPOSITION,
            pos,
            True
        )
        xStart = self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_POINTXFROMPOSITION,
            0,
            start
        )
        yStart = self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_POINTYFROMPOSITION,
            0,
            start
        )
        xEnd = self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_POINTXFROMPOSITION,
            0,
            end
        )
        line = self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_LINEFROMPOSITION,
            start
        )
        height = self.SendScintilla(
            _Qsci.QsciScintillaBase.SCI_TEXTHEIGHT,
            line
        )
        rect = _QtCore.QRect(xStart, yStart, xEnd-xStart, height)
        _QtWidgets.QToolTip.showText(ev.globalPos(), docString, self.viewport(), rect)

''' End Class '''

if __name__ == '__main__':
    import sys
    app = _QtWidgets.QApplication(sys.argv)
    _QtWidgets.QApplication.setStyle(_QtWidgets.QStyleFactory.create('Fusion'))
    myGUI = EditorWidget()
    myGUI.show()
    sys.exit(app.exec_())
