import re
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *



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
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#ff888888"))

        # Margin 1 = Symbol margin
        self.setMarginType(1, QsciScintilla.SymbolMargin)
        self.setMarginWidth(1, "00000")

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

    def foldAll(self):
        self.foldAll()

    def clearFolds(self):
        self.clearFolds()

    def foldCurrentMethod(self, lineNumber):
        self.foldLine(lineNumber)

    def setIndicatorHighlight(self):
        self._setIndicator(
            self.HIGHLIGHTINDICATOR,
            QColor(0, 255, 0, 80)
        )

    def index_strings_in_text(self, search_text,
                              text,
                              case_sensitive=False,
                              regular_expression=False,
                              text_to_bytes=False,
                              whole_words=False):
        """
        """
        # Check if whole words only should be matched
        if whole_words == True:
            search_text = r"\b(" + search_text + r")\b"
        # Convert text to bytes so that utf-8 characters will be parsed correctly
        if text_to_bytes == True:
            search_text = bytes(search_text, "utf-8")
            text = bytes(text, "utf-8")
        # Set the search text according to the regular expression selection
        if regular_expression == False:
            search_text = re.escape(search_text)
        # Compile expression according to case sensitivity flag
        if case_sensitive == True:
            compiled_search_re = re.compile(search_text)
        else:
            compiled_search_re = re.compile(search_text, re.IGNORECASE)
        # Create the list with all of the matches
        list_of_matches = [(0, match.start(), 0, match.end()) for match in re.finditer(compiled_search_re, text)]
        return list_of_matches

    def find_all(self,
                 searchText,
                 caseSensitive=False,
                 regular_expression=False,
                 text_to_bytes=False,
                 whole_words=False):
        """Find all instances of a string and return a list of (line, index_start, index_end)"""
        #Find all instances of the search string and return the list
        matches = self.index_strings_in_text(
            searchText,
            self.text(),
            caseSensitive,
            regular_expression,
            text_to_bytes,
            whole_words
        )
        return matches

    def highlight_raw(self, highlight_list):
        """
        Core highlight function that uses Scintilla messages to style indicators.
        QScintilla's fillIndicatorRange function is to slow for large numbers of
        highlights!
        INFO:   This is done using the scintilla "INDICATORS" described in the official
                scintilla API (http://www.scintilla.org/ScintillaDoc.html#Indicators)
        """
        scintilla_command = QsciScintillaBase.SCI_INDICATORFILLRANGE
        for highlight in highlight_list:
            start = highlight[1]
            length = highlight[3] - highlight[1]
            self.SendScintilla(
                scintilla_command,
                start,
                length
            )

    def find_text(self,
                  search_text,
                  case_sensitive=False,
                  search_forward=True,
                  regular_expression=False):
        def focus_entire_found_text():
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
        if regular_expression == True:
            # Get the absolute cursor index from line/index position
            line, index = self.getCursorPosition()
            absolute_position = self.positionFromLineIndex(line, index)
            # Compile the search expression according to the case sensitivity
            if case_sensitive == True:
                compiled_search_re = re.compile(search_text)
            else:
                compiled_search_re = re.compile(search_text, re.IGNORECASE)
            # Search based on the search direction
            if search_forward == True:
                # Regex search from the absolute position to the end for the search expression
                search_result = re.search(compiled_search_re, self.text()[absolute_position:])
                if search_result != None:
                    #Select the found expression
                    result_start    = absolute_position + search_result.start()
                    result_end      = result_start + len(search_result.group(0))
                    self.setCursorPosition(0, result_start)
                    self.setSelection(0, result_start, 0, result_end)
                    # Return successful find
                    return data.SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    search_result = re.search(compiled_search_re, self.text())
                    if search_result != None:
                        # Select the found expression
                        result_start    = search_result.start()
                        result_end      = result_start + len(search_result.group(0))
                        self.setCursorPosition(0, result_start)
                        self.setSelection(0, result_start, 0, result_end)
                        self.main_form.display.write_to_statusbar("Reached end of document, started from the top again!")
                        # Return cycled find
                        return data.SearchResult.CYCLED
                    else:
                        self.main_form.display.write_to_statusbar("Text was not found!")
                        return data.SearchResult.NOT_FOUND
            else:
                # Move the cursor one character back when searching backard
                # to not catch the same search result again
                cursor_position = self.get_absolute_cursor_position()
                search_text = self.text()[:cursor_position]
                # Regex search from the absolute position to the end for the search expression
                search_result = [m for m in re.finditer(compiled_search_re, search_text)]
                if search_result != []:
                    #Select the found expression
                    result_start    = search_result[-1].start()
                    result_end      = search_result[-1].end()
                    self.setCursorPosition(0, result_start)
                    self.setSelection(0, result_start, 0, result_end)
                    # Return successful find
                    return data.SearchResult.FOUND
                else:
                    # Begin a new search from the top of the document
                    search_result = [m for m in re.finditer(compiled_search_re, self.text())]
                    if search_result != []:
                        # Select the found expression
                        result_start    = search_result[-1].start()
                        result_end      = search_result[-1].end()
                        self.setCursorPosition(0, result_start)
                        self.setSelection(0, result_start, 0, result_end)
                        self.main_form.display.write_to_statusbar("Reached end of document, started from the top again!")
                        # Return cycled find
                        return data.SearchResult.CYCLED
                    else:
                        self.main_form.display.write_to_statusbar("Text was not found!")
                        return data.SearchResult.NOT_FOUND
        else:
            # Move the cursor one character back when searching backard
            # to not catch the same search result again
            if search_forward == False:
                line, index = self.getCursorPosition()
                self.setCursorPosition(line, index-1)
            # "findFirst" is the QScintilla function for finding text in a document
            search_result = self.findFirst(search_text,
                False,
                case_sensitive,
                False,
                False,
                forward=search_forward
            )
            if search_result == False:
                # Try to find text again from the top or at the bottom of
                # the scintilla document, depending on the search direction
                if search_forward == True:
                    s_line = 0
                    s_index = 0
                else:
                    s_line = len(self.line_list)-1
                    s_index = len(self.text())
                inner_result = self.findFirst(
                    search_text,
                    False,
                    case_sensitive,
                    False,
                    False,
                    forward=search_forward,
                    line=s_line,
                    index=s_index
                )
                if inner_result == False:
                    # self.main_form.display.write_to_statusbar("Text was not found!")
                    return -1
                else:
                    # self.main_form.display.write_to_statusbar("Reached end of document, started from the other end again!")
                    focus_entire_found_text()
                    # Return cycled find
                    return 2
            else:
                # Found text
                # self.main_form.display.write_to_statusbar("Found text: \"" + search_text + "\"")
                focus_entire_found_text()
                # Return successful find
                return 1

    def gotoLine(self, lineNumber):
        """
        Highlight selected line
        """
        lineText = self.getLineText(lineNumber)
        lineText.setSelection(lineNumber - 1, 0, lineNumber - 1, len(lineText))

    def highlightText(self,
                      highlightText,
                       caseSensitive=False,
                       regular_expression=False):
        """
        Highlight all instances of the selected text with a selected colour
        """
        #Setup the indicator style, the highlight indicator will be 0
        self.setIndicatorHighlight()
        #Get all instances of the text using list comprehension and the re module
        matches = self.find_all(
            highlightText,
            caseSensitive,
            regular_expression,
            text_to_bytes=True
        )
        #Check if the match list is empty
        if matches:
            #Use the raw highlight function to set the highlight indicators
            self.highlight_raw(matches)
            self.find_text(highlightText, caseSensitive, True, regular_expression)
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

    def find_and_replace(self,
                         search_text,
                         replace_text,
                         case_sensitive=False,
                         search_forward=True,
                         regular_expression=False):
        """Find next instance of the search string and replace it with the replace string"""
        if regular_expression == True:
            # Check if expression exists in the document
            search_result = self.find_text(
                search_text, case_sensitive, search_forward, regular_expression
            )
            if search_result != data.SearchResult.NOT_FOUND:
                if case_sensitive == True:
                    compiled_search_re = re.compile(search_text)
                else:
                    compiled_search_re = re.compile(search_text, re.IGNORECASE)
                # The search expression is already selected from the find_text function
                found_expression = self.selectedText()
                # Save the found selected text line/index information
                saved_selection = self.getSelection()
                # Replace the search expression with the replace expression
                replacement = re.sub(compiled_search_re, replace_text, found_expression)
                # Replace selected text with replace text
                self.replaceSelectedText(replacement)
                # Select the newly replaced text
                self.main_form.display.repl_display_message(replacement)
                self.setSelection(
                    saved_selection[0],
                    saved_selection[1],
                    saved_selection[2],
                    saved_selection[1] + len(replacement)
                )
                return True
            else:
                # Search text not found
                self.main_form.display.write_to_statusbar("Text was not found!")
                return False
        else:
            # Check if string exists in the document
            search_result = self.find_text(search_text, case_sensitive)
            if search_result != -1:
                # Save the found selected text line/index information
                saved_selection = self.getSelection()
                # Replace selected text with replace text
                self.replaceSelectedText(replace_text)
                # Select the newly replaced text
                self.setSelection(
                    saved_selection[0],
                    saved_selection[1],
                    saved_selection[2],
                    saved_selection[1] + len(replace_text)
                )
                return True
            else:
                # Search text not found
                print("Text was not found!")
                return False

    def clear_highlights(self):
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

    def _set_indicator(self,
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


    def set_indicator_replace(self):
        """Set the appearance of the highlight indicator"""
        self._set_indicator(
            self.REPLACE_INDICATOR,
            QColor(50, 180, 255, 80)
        )

    def replace_and_index(self, input_string,
                          search_text,
                          replace_text,
                          case_sensitive=False,
                          regular_expression=False):
        """
        Function that replaces the search text with replace text in a string,
        using regular expressions if specified, and returns the
        line numbers and indexes of the replacements as a list.
        """
        # First check if the replacement action is needed
        if search_text == replace_text and case_sensitive == True:
            return None, input_string
        elif search_text.lower() == replace_text.lower() and case_sensitive == False:
            return None, input_string
        # Initialize the return variables
        replaced_text = None
        # Find the search text matches that will be highlighted (pre-replacement)
        # Only when not searching with regular expressions
        if regular_expression == False:
            matches = self.index_strings_in_text(
                search_text,
                input_string,
                case_sensitive,
                regular_expression,
                text_to_bytes=True
            )
            # Create a matches list according to regular expression selection
        if regular_expression == True:
            # Compile the regular expression object according to the case sensitivity
            if case_sensitive == True:
                compiled_search_re = re.compile(search_text)
            else:
                compiled_search_re = re.compile(search_text, re.IGNORECASE)
            # Replace all instances of search text with the replace text
            replaced_text = re.sub(compiled_search_re, replace_text, input_string)
            replaced_match_indexes = []
            # Split old and new texts into line lists
            split_input_text = input_string.split("\n")
            split_replaced_text = replaced_text.split("\n")
            # Loop through the old text and compare it line-by-line to the old text
            try:
                for i in range(len(split_input_text)):
                    if split_input_text[i] != split_replaced_text[i]:
                        replaced_match_indexes.append(i)
            except:
                # If regular expression replaced lines,
                # then we cannot highlight the replacements
                replaced_match_indexes = []
        else:
            replaced_text = None
            if case_sensitive == True:
                # Standard string replace
                replaced_text = input_string.replace(search_text, replace_text)
            else:
                # Escape the regex special characters
                new_search_text = re.escape(search_text)
                # Replace backslashes with double backslashes, so that the
                # regular expression treats backslashes the same as standard
                # Python string replace!
                new_replace_text = replace_text.replace("\\", "\\\\")
                compiled_search_re = re.compile(new_search_text, re.IGNORECASE)
                replaced_text = re.sub(
                    compiled_search_re,
                    new_replace_text,
                    input_string
                )
            replaced_match_indexes = []
            # Loop while storing the new indexes
            diff = 0
            bl_search = bytes(search_text, "utf-8")
            bl_search = len(bl_search.replace(b"\\", b" "))
            bl_replace = bytes(replace_text, "utf-8")
            bl_replace = len(bl_replace.replace(b"\\", b" "))
            for i, match in enumerate(matches):
                # Subtract the length of the search text from the match index,
                # to offset the shortening of the whole text when the lenght
                # of the replace text is shorter than the search text
                diff = (bl_replace - bl_search) * i
                new_index = match[1] + diff
                # Check if the index correction went into a negative index
                if new_index < 0:
                    new_index = 0
                # The line is always 0, because Scintilla also allows
                # indexing over multiple lines! If the index number goes
                # over the length of a line, it "overflows" into the next line.
                # Basically this means that you can access any line/index by
                # treating the whole text not as a list of lines, but as an array.
                replaced_match_indexes.append(
                    (
                        0,
                        new_index,
                        0,
                        new_index + bl_replace
                    )
                )
        # Return the match list and the replaced text
        return replaced_match_indexes, replaced_text

    def replace_all(self,
                    search_text,
                    replace_text,
                    case_sensitive=False,
                    regular_expression=False):
        """Replace all occurences of a string in a scintilla document"""
        # Store the current cursor position
        current_position = self.getCursorPosition()
        # Move cursor to the top of the document, so all the search string instances will be found
        self.setCursorPosition(0, 0)
        # Clear all previous highlights
        self.clear_highlights()
        # Setup the indicator style, the replace indicator is 1
        self.set_indicator_replace()
        # Correct the displayed file name
        file_name = self.filePath
        # if self.save_name == None or self.save_name == "":
        #     file_name = self.parent.tabText(self.parent.currentIndex())
        # else:
        #     file_name = os.path.basename(self.save_name)
        # Check if there are any instances of the search text in the document
        # based on the regular expression flag
        search_result = None
        if regular_expression == True:
            # Check case sensitivity for regular expression
            if case_sensitive == True:
                compiled_search_re = re.compile(search_text)
            else:
                compiled_search_re = re.compile(search_text, re.IGNORECASE)
            search_result = re.search(compiled_search_re, self.text())
        else:
            search_result = self.find_text(search_text, case_sensitive)
        if search_result == -1:
            message = "No matches were found in '{}'!".format(file_name)
            print(message)
            return
        # Use the re module to replace the text
        text = self.text()
        matches, replaced_text = self.replace_and_index(
            text,
            search_text,
            replace_text,
            case_sensitive,
            regular_expression,
        )
        # Check if there were any matches or
        # if the search and replace text were equivalent!
        if matches != None:
            # Replace the text
            self._replaceEntireText(replaced_text)
            # Matches can only be displayed for non-regex functionality
            if regular_expression == True:
                # Build the list of matches used by the highlight_raw function
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
                    self.main_form.display.repl_display_message(
                        message,
                        message_type=data.MessageType.SUCCESS
                    )
                    for match in corrected_matches:
                        line = self.lineIndexFromPosition(match[1])[0] + 1
                        index = self.lineIndexFromPosition(match[1])[1]
                        message = "    replacement made in line:{:d}".format(line)
                        self.main_form.display.repl_display_message(
                            message,
                            message_type=data.MessageType.SUCCESS
                        )
                else:
                    message = "{:d} replacements made in {}!\n".format(
                        len(corrected_matches),
                        file_name
                    )
                    message += "Too many to list individually!"
                    self.main_form.display.repl_display_message(
                        message,
                        message_type=data.MessageType.WARNING
                    )
                # Highlight and display the line difference between the old and new texts
                self.highlight_raw(corrected_matches)
            else:
                # Display the replacements in the REPL tab
                if len(matches) < settings.Editor.maximum_highlights:
                    message = "{} replacements:".format(file_name)
                    print(message)
                    for match in matches:
                        line = self.lineIndexFromPosition(match[1])[0] + 1
                        index = self.lineIndexFromPosition(match[1])[1]
                        message = "    replaced \"{}\" in line:{:d} column:{:d}".format(
                            search_text,
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
                self.highlight_raw(matches)
            # Restore the previous cursor position
            self.setCursorPosition(current_position[0], current_position[1])
        else:
            message = "The search string and replace string are equivalent!\n"
            message += "Change the search/replace string or change the case sensitivity!"
            print(message)

    def replace_in_selection(self,
                             search_text,
                             replace_text,
                             case_sensitive=False,
                             regular_expression=False):
        """Replace all occurences of a string in the current selection in the scintilla document"""
        # Get the start and end point of the selected text
        start_line, start_index, end_line, end_index = self.getSelection()
        # Get the currently selected text and use the re module to replace the text
        selected_text = self.selectedText()
        replaced_text = functions.regex_replace_text(
            selected_text,
            search_text,
            replace_text,
            case_sensitive,
            regular_expression
        )
        # Check if any replacements were made
        if replaced_text != selected_text:
            # Put the text back into the selection space and select it again
            self.replaceSelectedText(replaced_text)
            new_end_line = start_line
            new_end_index = start_index + len(bytearray(replaced_text, "utf-8"))
            self.setSelection(start_line, start_index, new_end_line, new_end_index)
        else:
            message = "No replacements were made!"
            self.main_form.display.repl_display_message(
                message,
                message_type=data.MessageType.WARNING
            )

    def _replaceEntireText(self, newText):
        """Replace the entire text of the document"""
        # Select the entire text
        self.selectAll(True)
        # Replace the text with the new
        self.replaceSelectedText(newText)

    def find(self, findText, findAll=False):
        if findAll:
            self.find_all(findText)
        else:
            self.find_text(findText)

    def replace(self, findText, replaceText, replaceAll=False):
        if replaceAll:
            self.replace_all(findText, replaceText)
        else:
            self.find_and_replace(findText, replaceText)

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