
# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2018 Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

##  FILE DESCRIPTION:
##      Water theme

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
name = "Water"
tooltip = "Water"
image_file = "tango_icons/theme-water.png"

Form = "#295a88"
Context_Menu_Background = QColor(0x29, 0x5a, 0x88)
Cursor = QColor(0xffffffff)
Cursor_Line_Background = QColor(0x72, 0x9f, 0xcf, 80)
Settings_Background = QColor("#3b82c4")
Settings_Label_Background = QColor(0x29, 0x5a, 0x88)
Settings_Hex_Edge = QColor("#e6e6e6")
Settings_Hex_Background = QColor(0x29, 0x5a, 0x88)
YesNoDialog_Edge = QColor("#e6e6e6")
YesNoDialog_Background = QColor("#3b82c4")


class FoldMargin:
    ForeGround = QColor(0xff4096bf)
    BackGround = QColor(0xff3476a3)


class LineMargin:
    ForeGround = QColor(0xffffffff)
    BackGround = QColor(0xff1f4661)


class Indication:
    Font = "#e6e6e6"
    ActiveBackGround = "#112435"
    ActiveBorder = "#e6e6e6"
    PassiveBackGround = "#295a88"
    PassiveBorder = "#33aaff"


class TextDifferColors:
    Indicator_Unique_1_Color = QColor(0x72, 0x9f, 0xcf, 80)
    Indicator_Unique_2_Color = QColor(0xad, 0x7f, 0xa8, 80)
    Indicator_Similar_Color = QColor(0x8a, 0xe2, 0x34, 80)

    
class Font:
    Default = QColor(0xffffffff)

    class Python:
        ClassName = ('Courier', 0xff5abcd8, 10, None)
        Comment = ('Courier', 0xff6cab9d, 10, None)
        CommentBlock = ('Courier', 0xff7f7f7f, 10, None)
        Decorator = ('Courier', 0xff805000, 10, None)
        Default = ('Courier', 0xffffffff, 10, None)
        DoubleQuotedString = ('Courier', 0xffc4bbb8, 10, None)
        FunctionMethodName = ('Courier', 0xff74ccf4, 10, None)
        HighlightedIdentifier = ('Courier', 0xff407090, 10, None)
        Identifier = ('Courier', 0xffffffff, 10, None)
        Inconsistent = ('Courier', 0xff6cab9d, 10, None)
        Keyword = ('Courier', 0xff2389da, 10, None)
        NoWarning = ('Courier', 0xff808080, 10, None)
        Number = ('Courier', 0xff74ccf4, 10, None)
        Operator = ('Courier', 0xffffffff, 10, None)
        SingleQuotedString = ('Courier', 0xffc4bbb8, 10, None)
        Spaces = ('Courier', 0xffc4bbb8, 10, None)
        Tabs = ('Courier', 0xffc4bbb8, 10, None)
        TabsAfterSpaces = ('Courier', 0xff74ccf4, 10, None)
        TripleDoubleQuotedString = ('Courier', 0xfff5b0cb, 10, None)
        TripleSingleQuotedString = ('Courier', 0xfff5b0cb, 10, None)
        UnclosedString = ('Courier', 0xffffffff, 10, None)
        CustomKeyword = ('Courier', 0xff6e6e00, 10, True)

class Paper:
    Default = QColor(0xff112435)

    class Python:
        TripleDoubleQuotedString = 0xff112435
        FunctionMethodName = 0xff112435
        TabsAfterSpaces = 0xff112435
        Tabs = 0xff112435
        Decorator = 0xff112435
        NoWarning = 0xff112435
        UnclosedString = 0xffe0c0e0
        Spaces = 0xff112435
        CommentBlock = 0xff112435
        Comment = 0xff112435
        TripleSingleQuotedString = 0xff112435
        SingleQuotedString = 0xff112435
        Inconsistent = 0xff112435
        Default = 0xff112435
        DoubleQuotedString = 0xff112435
        Operator = 0xff112435
        Number = 0xff112435
        Identifier = 0xff112435
        ClassName = 0xff112435
        Keyword = 0xff112435
        HighlightedIdentifier = 0xff112435
        CustomKeyword = 0xff112435
     



