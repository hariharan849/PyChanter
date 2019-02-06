import re
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *



class SearchResult:
    NOT_FOUND   = None
    FOUND       = 1
    CYCLED      = 2


class CustomTab(QTabWidget):
    def __init__(self, parent=None):
        super(CustomTab, self).__init__(parent)

    def textChangedSlot(self):
        if self.currentWidget() == None:
            return
        if not isinstance(self.currentWidget(), EditorWidget):
            return
        if self.currentWidget().isEdited:
            return
        self.currentWidget().isEdited = True
        self.setTabText(self.currentIndex(), self.tabText(self.currentIndex()) + "*")

class EditorWidget(QsciScintilla):
    isEdited = False
    HIGHLIGHTINDICATOR = 0
    FIND_INDICATOR = 2
    REPLACE_INDICATOR = 3
    def __init__(self, parent=None, filePath=None):
        print (dir(QsciScintilla))
        super(EditorWidget, self).__init__(parent)

        # -------------------------------- #
        #           Window setup           #
        # -------------------------------- #

        # 1. Define the geometry of the main window
        # ------------------------------------------
        self.setWindowTitle("QScintilla Test")

        # 2. Create layout
        # ---------------------------
        self.__lyt = QVBoxLayout(self)

        self.__myFont = QFont()
        self.__myFont.setPointSize(14)

        # -------------------------------- #
        #     QScintilla editor setup      #
        # -------------------------------- #
        self.setFolding(self.BoxedTreeFoldStyle)

        # ! Make instance of QSciScintilla class!
        # ----------------------------------------
        # self.__editor = QsciScintilla()
        fileData = ""
        if filePath:
            if isinstance(filePath, list):
                fileData = open(filePath[0]).read()
            else:
                fileData = open(filePath).read()
        self.setText(fileData)
        self.filePath = filePath

        self.lexer = QsciLexerPython()
        self.setLexer(self.lexer)
        self.setUtf8(True)             # Set encoding to UTF-8
        self.setFont(self.__myFont)

        # 1. Text wrapping
        # -----------------
        self.setWrapMode(QsciScintilla.WrapWord)
        self.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.setWrapIndentMode(QsciScintilla.WrapIndentIndented)

        # 2. End-of-line mode
        # --------------------
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)

        # 3. Indentation
        # ---------------
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)

        # 4. Caret
        # ---------
        self.setCaretForegroundColor(QColor("#ff0000ff"))
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#1f0000ff"))
        self.setCaretWidth(2)

        # 5. Margins
        # -----------
        # Margin 0 = Line nr margin
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0")
        self.setMarginsForegroundColor(QColor("#ff888888"))

        # Margin 1 = Symbol margin
        self.setMarginType(1, QsciScintilla.SymbolMargin)
        self.setMarginWidth(1, "00")

        self.markerDefine(QsciScintilla.Circle, 3)

        self.setMarginMarkerMask(1, 0b1111)

        # 6. Margin mouse clicks
        # -----------------------
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.__margin_left_clicked)
        self.marginRightClicked.connect(self.__margin_right_clicked)


        # ! Add editor to layout !
        # -------------------------
        # self.__lyt.addWidget(self.__editor)
        self.showMaximized()
        self.show()

        import os as _os
        styleFile = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'resources', 'styleSheet', 'QTDark1.stylesheet')
        with open(styleFile, "r") as fh:
            self.setStyleSheet(fh.read())

    ''''''

    def getLineText(self, lineNumber):
        """
        Return the text of the selected line in the scintilla document
        """
        lineText = self.text(lineNumber - 1)
        return lineText.replace("\n", "")

    def togglecommentLine(self, lineNumber):
        """
        Toggle comment/uncomment line for the passed line number
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
        """
        lineText = self.getLineText(startLineNumber)
        comment = False
        if lineText.startswith('#'):
            comment = True
        for lineNumber in range(startLineNumber, endLineNumber+1):
            lineText = self.getLineText(lineNumber)
            self.setSelection(lineNumber - 1, 0, lineNumber, 0)
            if comment:
                self.replaceSelectedText(lineText[1:] + "\n")
            else:
                self.replaceSelectedText('#' + lineText + "\n")

        self.setCursorPosition(endLineNumber - 1, 0)

    def _setIndicator(self, indicator, foreColor):
        """
        Set the indicator settings
        """
        self.indicatorDefine(
            QsciScintillaBase.INDIC_ROUNDBOX,
            indicator
        )
        self.setIndicatorForegroundColor(
            foreColor,
            indicator
        )
        self.SendScintilla(
            QsciScintillaBase.SCI_SETINDICATORCURRENT,
            indicator
        )

    def moveLineDown(self):
        self.SendScintilla(QsciScintilla.SCI_LINECUT)
        self.SendScintilla(QsciScintilla.SCI_LINEDOWN)
        self.SendScintilla(QsciScintilla.SCI_PASTE)
        self.SendScintilla(QsciScintilla.SCI_LINEUP)

    def moveLineUp(self):
        self.SendScintilla(QsciScintilla.SCI_LINECUT)
        self.SendScintilla(QsciScintilla.SCI_LINEUP)
        self.SendScintilla(QsciScintilla.SCI_PASTE)
        self.SendScintilla(QsciScintilla.SCI_LINEUP)

    def foldEntireFile(self):
        self.foldAll()

    def clearAllFoldings(self):
        self.clearFolds()

    def foldCurrentMethod(self, lineNumber):
        self.foldLine(lineNumber)

    def setIndicatorHighlight(self):
        self._setIndicator(
            self.HIGHLIGHTINDICATOR,
            QColor(0, 255, 0, 80)
        )

    def indexStringsInText(self, searchText, text, caseSensitive=False, regularExpression=False, textToBytes=False, wholeWords=False):
        """
        """
        # Check if whole words only should be matched
        if wholeWords == True:
            searchText = r"\b(" + searchText + r")\b"
        # Convert text to bytes so that utf-8 characters will be parsed correctly
        if textToBytes == True:
            searchText = bytes(searchText, "utf-8")
            text = bytes(text, "utf-8")
        # Set the search text according to the regular expression selection
        if regularExpression == False:
            searchText = re.escape(searchText)
        # Compile expression according to case sensitivity flag
        if caseSensitive == True:
            compiledSearchRe = re.compile(searchText)
        else:
            compiledSearchRe = re.compile(searchText, re.IGNORECASE)
        # Create the list with all of the matches
        listOfMatches = [(0, match.start(), 0, match.end()) for match in re.finditer(compiledSearchRe, text)]
        return listOfMatches

    def findAll(self, searchText, caseSensitive=False, regularExpression=False, textToBytes=False, wholeWords=False):
        """Find all instances of a string and return a list of (line, index_start, index_end)"""
        #Find all instances of the search string and return the list
        matches = self.indexStringsInText(
            searchText,
            self.text(),
            caseSensitive,
            regularExpression,
            textToBytes,
            wholeWords
        )
        return matches

    def highlightRaw(self, highlightList):
        """
        Core highlight function that uses Scintilla messages to style indicators.
        QScintilla's fillIndicatorRange function is to slow for large numbers of
        highlights!
        INFO:   This is done using the scintilla "INDICATORS" described in the official
                scintilla API (http://www.scintilla.org/ScintillaDoc.html#Indicators)
        """
        scintillaCommand = QsciScintillaBase.SCI_INDICATORFILLRANGE
        for highlight in highlightList:
            start = highlight[1]
            length = highlight[3] - highlight[1]
            self.SendScintilla(
                scintillaCommand,
                start,
                length
            )

    def findText(self, searchText, caseSensitive=False, searchForward=True, regularExpression=False):
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
                compiledSearchRe = re.compile(searchText)
            else:
                compiledSearchRe = re.compile(searchText, re.IGNORECASE)
            # Search based on the search direction
            if searchForward == True:
                # Regex search from the absolute position to the end for the search expression
                searchResult = re.search(compiledSearchRe, self.text()[absolutePosition:])
                if searchResult != None:
                    #Select the found expression
                    resultStart    = absolutePosition + searchResult.start()
                    resultEnd      = resultStart + len(searchResult.group(0))
                    self.setCursorPosition(0, resultStart)
                    self.setSelection(0, resultStart, 0, resultEnd)
                    # Return successful find
                    return SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    searchResult = re.search(compiledSearchRe, self.text())
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
                searchResult = [m for m in re.finditer(compiledSearchRe, searchText)]
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
                    searchResult = [m for m in re.finditer(compiledSearchRe, self.text())]
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
        Highlight selected line
        """
        lineText = self.getLineText(lineNumber)
        lineText.setSelection(lineNumber - 1, 0, lineNumber - 1, len(lineText))

    def highlightText(self, highlightText, caseSensitive=False, regularExpression=False):
        """
        Highlight all instances of the selected text with a selected colour
        """
        #Setup the indicator style, the highlight indicator will be 0
        self.setIndicatorHighlight()
        #Get all instances of the text using list comprehension and the re module
        matches = self.findAll(
            highlightText,
            caseSensitive,
            regularExpression,
            textToBytes=True
        )
        #Check if the match list is empty
        if matches:
            #Use the raw highlight function to set the highlight indicators
            self.highlightRaw(matches)
            self.findText(highlightText, caseSensitive, True, regularExpression)
        else:
            print ("no Matches")

    def convertCase(self, caseType='l'):
        """Convert selected text in the scintilla document into the selected case letters"""
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

    def findAndReplace(self, searchText, replaceText, caseSensitive=False, searchForward=True, regularExpression=False):
        """Find next instance of the search string and replace it with the replace string"""
        if regularExpression == True:
            # Check if expression exists in the document
            searchResult = self.findText(
                searchText, caseSensitive, searchForward, regularExpression
            )
            if searchResult != SearchResult.NOT_FOUND:
                if caseSensitive == True:
                    compiledSearchRe = re.compile(searchText)
                else:
                    compiledSearchRe = re.compile(searchText, re.IGNORECASE)
                # The search expression is already selected from the findText function
                found_expression = self.selectedText()
                # Save the found selected text line/index information
                savedSelection = self.getSelection()
                # Replace the search expression with the replace expression
                replacement = re.sub(compiledSearchRe, replaceText, found_expression)
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
            searchResult = self.findText(searchText, caseSensitive)
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
        """Clear all highlighted text"""
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

    def _setIndicator(self,
                       indicator,
                       fore_color):
        """Set the indicator settings"""
        self.indicatorDefine(
            QsciScintillaBase.INDIC_ROUNDBOX,
            indicator
        )
        self.setIndicatorForegroundColor(
            fore_color,
            indicator
        )
        self.SendScintilla(
            QsciScintillaBase.SCI_SETINDICATORCURRENT,
            indicator
        )


    def setIndicatorReplace(self):
        """Set the appearance of the highlight indicator"""
        self._setIndicator(
            self.REPLACE_INDICATOR,
            QColor(50, 180, 255, 80)
        )

    def replaceAndIndex(self, inputString, searchText, replaceText, caseSensitive=False, regularExpression=False):
        """
        Function that replaces the search text with replace text in a string,
        using regular expressions if specified, and returns the
        line numbers and indexes of the replacements as a list.
        """
        # First check if the replacement action is needed
        if searchText == replaceText and caseSensitive == True:
            return None, inputString
        elif searchText.lower() == replaceText.lower() and caseSensitive == False:
            return None, inputString
        # Initialize the return variables
        replacedText = None
        # Find the search text matches that will be highlighted (pre-replacement)
        # Only when not searching with regular expressions
        if regularExpression == False:
            matches = self.indexStringsInText(
                searchText,
                inputString,
                caseSensitive,
                regularExpression,
                textToBytes=True
            )
            # Create a matches list according to regular expression selection
        if regularExpression == True:
            # Compile the regular expression object according to the case sensitivity
            if caseSensitive == True:
                compiledSearchRe = re.compile(searchText)
            else:
                compiledSearchRe = re.compile(searchText, re.IGNORECASE)
            # Replace all instances of search text with the replace text
            replacedText = re.sub(compiledSearchRe, replaceText, inputString)
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
            if caseSensitive == True:
                # Standard string replace
                replacedText = inputString.replace(searchText, replaceText)
            else:
                # Escape the regex special characters
                newSearchText = re.escape(searchText)
                # Replace backslashes with double backslashes, so that the
                # regular expression treats backslashes the same as standard
                # Python string replace!
                newReplaceText = replaceText.replace("\\", "\\\\")
                compiledSearchRe = re.compile(newSearchText, re.IGNORECASE)
                replacedText = re.sub(
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

    def replaceAll(self, searchText, replaceText, caseSensitive=False, regularExpression=False):
        """Replace all occurences of a string in a scintilla document"""
        # Store the current cursor position
        currentPosition = self.getCursorPosition()
        # Move cursor to the top of the document, so all the search string instances will be found
        self.setCursorPosition(0, 0)
        # Clear all previous highlights
        self._clearHighlights()
        # Setup the indicator style, the replace indicator is 1
        self.setIndicatorReplace()
        # Correct the displayed file name
        file_name = self.filePath
        # if self.save_name == None or self.save_name == "":
        #     file_name = self.parent.tabText(self.parent.currentIndex())
        # else:
        #     file_name = os.path.basename(self.save_name)
        # Check if there are any instances of the search text in the document
        # based on the regular expression flag
        searchResult = None
        if regularExpression == True:
            # Check case sensitivity for regular expression
            if caseSensitive == True:
                compiledSearchRe = re.compile(searchText)
            else:
                compiledSearchRe = re.compile(searchText, re.IGNORECASE)
            searchResult = re.search(compiledSearchRe, self.text())
        else:
            searchResult = self.findText(searchText, caseSensitive)
        if searchResult == -1:
            message = "No matches were found in '{}'!".format(file_name)
            print(message)
            return
        # Use the re module to replace the text
        text = self.text()
        matches, replacedText = self.replaceAndIndex(
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
                self.highlightRaw(corrected_matches)
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
                self.highlightRaw(matches)
            # Restore the previous cursor position
            self.setCursorPosition(currentPosition[0], currentPosition[1])
        else:
            message = "The search string and replace string are equivalent!\n"
            message += "Change the search/replace string or change the case sensitivity!"
            print(message)

    def replaceInSelection(self, searchText, replaceText, caseSensitive=False, regularExpression=False):
        """Replace all occurences of a string in the current selection in the scintilla document"""
        # Get the start and end point of the selected text
        startLine, startIndex, end_line, end_index = self.getSelection()
        # Get the currently selected text and use the re module to replace the text
        selected_text = self.selectedText()
        replacedText = functions.regex_replaceText(
            selected_text,
            searchText,
            replaceText,
            caseSensitive,
            regularExpression
        )
        # Check if any replacements were made
        if replacedText != selected_text:
            # Put the text back into the selection space and select it again
            self.replaceSelectedText(replacedText)
            newEndLine = startLine
            newEndIndex = startIndex + len(bytearray(replacedText, "utf-8"))
            self.setSelection(startLine, startIndex, newEndLine, newEndIndex)
        else:
            message = "No replacements were made!"
            print (message)

    def _replaceEntireText(self, newText):
        """Replace the entire text of the document"""
        # Select the entire text
        self.selectAll(True)
        # Replace the text with the new
        self.replaceSelectedText(newText)

    def find(self, findText, findAll=False):
        if findAll:
            self.findAll(findText)
        else:
            self.findText(findText)

    def replace(self, findText, replaceText, replaceAll=False):
        if replaceAll:
            self.replaceAll(findText, replaceText)
        else:
            self.findAndReplace(findText, replaceText)

    def __margin_left_clicked(self, margin_nr, line_nr, state):
        print("Margin clicked (left mouse btn)!")
        print(" -> margin_nr: " + str(margin_nr))
        print(" -> line_nr:   " + str(line_nr))
        # print("", state)

        if state == Qt.ControlModifier:
            # Show green dot.
            self.markerAdd(line_nr, 0)

        elif state == Qt.ShiftModifier:
            # Show green arrow.
            self.markerAdd(line_nr, 1)

        elif state == Qt.AltModifier:
            # Show red dot.
            self.markerAdd(line_nr, 2)

        else:
            # Show red arrow.

            if self.markersAtLine(line_nr) == 8:
                self.markerDelete(line_nr, 3)
            else:
                self.markerAdd(line_nr, 3)

    ''''''

    def __margin_right_clicked(self, margin_nr, line_nr, state):
        print("Margin clicked (right mouse btn)!")
        print(" -> margin_nr: " + str(margin_nr))
        print(" -> line_nr:   " + str(line_nr))
        print("")

    ''''''

    def __btn_action(self):
        print("Hello World!")

    ''''''


''' End Class '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    myGUI = EditorWidget()

    sys.exit(app.exec_())