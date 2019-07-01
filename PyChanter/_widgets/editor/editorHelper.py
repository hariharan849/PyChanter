"""
Scintilla Editor helper widgets goes here
"""
import ast as _ast
import re as _re
from PyQt5 import (
    QtWidgets as _QtWidgets,
    QtGui as _QtGui
    )
from PyChanter import constants as _constants
from . import water as _water


class PythonNode(object):
    """
    Wrapper to hold node information
    """
    def __init__(self, name, type, lineNumber, level):
        self.name = name
        self.type = type
        self.lineNumber = lineNumber
        self.level = level
        self.children = []


class PythonModuleInfo(_QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(PythonModuleInfo, self).__init__(parent)

    def createModuleTree(self, text):
        """
        Show the node tree of a parsed file in a "PythonModuleInfo" tree
        display widget in the upper window
        """
        # Check if the custom editor is valid
        # with open(modulePath, 'r') as fileObj:
        #     text = fileObj.read()
        if not text:
            _QtWidgets.QMessageBox.warning(self, 'Error', "Empty Document in file",
                                buttons=QMessageBox.Ok)
            return
        # Define a name for the NODE tab
        node_tree_tab_name = "Module Info"

        # Get all the file information
        try:
            moduleTree = parsePythonModule(text)
            parseError = False
        except Exception as ex:
            # Exception, probably an error in the file's syntax
            moduleTree = []
            parseError = ex
        # Display the information in the tree tab
        self._setDisplayModel(
            moduleTree,
            parseError
        )

    def _setDisplayModel(self, moduleTree, parseError=False):
        """
        Display the input python data in the tree display
        """
        # Define the display structure texts
        importVarText = "IMPORTS MODULES:"
        globalVarText = "GLOBALS VARIABLS:"
        classVarText = "CLASS INFORMATION:"
        functionVarText = "FUNCTIONS INFORMATION:"
        # Initialize the tree display to Python file type
        self.setSelectionBehavior(_QtWidgets.QAbstractItemView.SelectRows)
        moduleTreeModel = _QtGui.QStandardItemModel()
        self.header().hide()
        self.setModel(moduleTreeModel)
        self.setUniformRowHeights(True)
        self._setFontSize()
        # Set the label properties
        labelBrush = _QtGui.QBrush(
            _QtGui.QColor(_water.Font.Python.SingleQuotedString[1])
        )
        labelFont = _QtGui.QFont(
            "Courier", _constants.defaultDirectoryFontSize, _QtGui.QFont.Bold
        )
        # Check if there was a parsing error
        if parseError != False:
            errorBrush = _QtGui.QBrush(_QtGui.QColor(180, 0, 0))
            errorFont = _QtGui.QFont(
                "Courier", _constants.defaultDirectoryFontSize, _QtGui.QFont.Bold
            )
            moduleTreeError = _QtGui.QStandardItem("ERROR PARSING FILE!")
            moduleTreeError.setEditable(False)
            moduleTreeError.setForeground(errorBrush)
            moduleTreeError.setFont(errorFont)
            # moduleTreeError.setIcon(self.node_icon_nothing)
            moduleTreeModel.appendRow(moduleTreeError)
            # Show the error message
            errorFont = _QtGui.QFont("Courier", _constants.defaultDirectoryFontSize)
            moduleTreeErrorMsg = _QtGui.QStandardItem(str(parseError))
            moduleTreeErrorMsg.setEditable(False)
            moduleTreeErrorMsg.setForeground(errorBrush)
            moduleTreeErrorMsg.setFont(errorFont)
            try:
                lineNumber = int(_re.search(r"line (\d+)", str(parseError)).group(1))
                moduleTreeErrorMsg.lineNumber = lineNumber
            except:
                pass
            moduleTreeModel.appendRow(moduleTreeErrorMsg)
            return
        # Create the filtered node lists
        importNodes = [x for x in moduleTree if x.type == "import"]
        classNodes = [x for x in moduleTree if x.type == "class"]
        functionNodes = [x for x in moduleTree if x.type == "function"]
        globalNodes = [x for x in moduleTree if x.type == "global_variable"]
        
        """Imported module filtering"""
        itemImports = _QtGui.QStandardItem(importVarText)
        itemImports.setEditable(False)
        itemImports.setForeground(labelBrush)
        itemImports.setFont(labelFont)
        for node in importNodes:
            importNodeText = str(node.name) + " (line:"
            importNodeText += str(node.lineNumber) + ")"
            itemImportNode = _QtGui.QStandardItem(importNodeText)
            itemImportNode.setEditable(False)
            # itemImportNode.setIcon(self.node_icon_import)
            itemImports.appendRow(itemImportNode)
        if importNodes == []:
            itemNoImportNode = _QtGui.QStandardItem("No imports found")
            itemNoImportNode.setEditable(False)
            # itemNoImportNode.setIcon(self.node_icon_nothing)
            itemImports.appendRow(itemNoImportNode)
        # Append the import node to the model
        moduleTreeModel.appendRow(itemImports)
        if importNodes == []:
            self.expand(itemImports.index())
            
        """Global variable nodes filtering"""
        itemGlobals = _QtGui.QStandardItem(globalVarText)
        itemGlobals.setEditable(False)
        itemGlobals.setForeground(labelBrush)
        itemGlobals.setFont(labelFont)
        # Check if there were any nodes found
        if globalNodes == []:
            itemNoGlobals = _QtGui.QStandardItem("No global variables found")
            itemNoGlobals.setEditable(False)
            itemGlobals.appendRow(itemNoGlobals)
        else:
            # Create the function nodes and add them to the tree
            for node in globalNodes:
                itemGlobals.appendRow(self._createChildNodes(node))
        # Append the function nodes to the model
        moduleTreeModel.appendRow(itemGlobals)
        if globalNodes == []:
            self.expand(itemGlobals.index())
        """Class nodes filtering"""
        itemClasses = _QtGui.QStandardItem(classVarText)
        itemClasses.setEditable(False)
        itemClasses.setForeground(labelBrush)
        itemClasses.setFont(labelFont)
        # Check if there were any nodes found
        if classNodes == []:
            itemNoClasses = _QtGui.QStandardItem("No classes found")
            itemNoClasses.setEditable(False)
            itemClasses.appendRow(itemNoClasses)
        else:
            # Create the class nodes and add them to the tree
            for node in classNodes:
                itemClasses.appendRow(self._createChildNodes(node))
        # Append the class nodes to the model
        moduleTreeModel.appendRow(itemClasses)
        
        """Function nodes filtering"""
        itemFunctions = _QtGui.QStandardItem(functionVarText)
        itemFunctions.setEditable(False)
        itemFunctions.setForeground(labelBrush)
        itemFunctions.setFont(labelFont)
        # Check if there were any nodes found
        if functionNodes == []:
            itemNoFunctions = _QtGui.QStandardItem("No functions found")
            itemNoFunctions.setEditable(False)
            itemFunctions.appendRow(itemNoFunctions)
        else:
            # Create the function nodes and add them to the tree
            for node in functionNodes:
                itemFunctions.appendRow(self._createChildNodes(node))
        # Append the function nodes to the model
        moduleTreeModel.appendRow(itemFunctions)
        # Expand the base nodes
        self.expand(itemClasses.index())
        self.expand(itemFunctions.index())
        # Resize the header so the horizontal scrollbar will have the correct width
        self.resizeColumnToContents(0)


    def _setFontSize(self):
        """Set the font size for the tree display items"""
        #Initialize the font with the new size
        font = _QtGui.QFont('Courier', _constants.defaultDirectoryFontSize)
        self.setFont(font)

    def _createChildNodes(self, node):
        # Construct the node text
        nodeText = str(node.name) + " (line:"
        nodeText += str(node.lineNumber) + ")"
        treeNode = _QtGui.QStandardItem(nodeText)
        treeNode.setEditable(False)
        for childNode in node.children:
            treeNode.appendRow(self._createChildNodes(childNode))
        # Sort the child node alphabetically
        treeNode.sortChildren(0)
        # Return the node
        return treeNode

def parsePythonModule(moduleText):
    """
    Parse the text and return nodes as a nested tree.
    The text must be valid Python 3 code.
    """

    # Main parsing function
    def parseModuleNode(astNode, level, parentNode=None):
        nonlocal globalsList
        nonlocal moduleNodeTree
        newNode = None
        if isinstance(astNode, _ast.ClassDef):
            newNode = PythonNode(
                astNode.name,
                "class",
                astNode.lineno,
                level
            )
            for childNode in astNode.body:
                result = parseModuleNode(childNode, level + 1, newNode)
                if result != None:
                    if isinstance(result, list):
                        for n in result:
                            newNode.children.append(n)
                    else:
                        newNode.children.append(result)
            newNode.children = sorted(newNode.children, key=lambda x: x.name)
        elif isinstance(astNode, _ast.FunctionDef):
            newNode = PythonNode(
                astNode.name,
                "function",
                astNode.lineno,
                level
            )
            for childNode in astNode.body:
                result = parseModuleNode(childNode, level + 1, newNode)
                if result != None:
                    if isinstance(result, list):
                        for n in result:
                            newNode.children.append(n)
                    else:
                        newNode.children.append(result)
            newNode.children = sorted(newNode.children, key=lambda x: x.name)
        elif isinstance(astNode, _ast.Import):
            newNode = PythonNode(
                astNode.names[0].name,
                "import",
                astNode.lineno,
                level
            )
        elif isinstance(astNode, _ast.Assign) and (level == 0 or parentNode == None):
            # Globals that do are not defined with the 'global' keyword,
            # but are defined on the top level
            newNodes = []
            for target in astNode.targets:
                if hasattr(target, "id") == True:
                    name = target.id
                    if not (name in globalsList):
                        newNodes.append(
                            PythonNode(
                                name,
                                "global_variable",
                                astNode.lineno,
                                level
                            )
                        )
                        globalsList.append(name)
            return newNodes
        elif isinstance(astNode, _ast.Global):
            # Globals can be nested somewhere deep in the AST, so they
            # are appended directly into the non-local moduleNodeTree list
            for name in astNode.names:
                if not (name in globalsList):
                    moduleNodeTree.append(
                        PythonNode(
                            name,
                            "global_variable",
                            astNode.lineno,
                            level
                        )
                    )
                    globalsList.append(name)
        else:
            if parentNode != None and hasattr(astNode, "body"):
                for childNode in astNode.body:
                    result = parseModuleNode(childNode, level + 1, parentNode)
                    if result != None:
                        if isinstance(result, list):
                            for n in result:
                                parentNode.children.append(n)
                        else:
                            parentNode.children.append(result)
                parentNode.children = sorted(parentNode.children, key=lambda x: x.name)
            else:
                newNodes = []
                if hasattr(astNode, "body"):
                    for childNode in astNode.body:
                        result = parseModuleNode(childNode, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    newNodes.append(n)
                            else:
                                newNodes.append(result)
                if hasattr(astNode, "orelse"):
                    for childNode in astNode.orelse:
                        result = parseModuleNode(childNode, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    newNodes.append(n)
                            else:
                                newNodes.append(result)
                if hasattr(astNode, "finalbody"):
                    for childNode in astNode.finalbody:
                        result = parseModuleNode(childNode, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    newNodes.append(n)
                            else:
                                newNodes.append(result)
                if hasattr(astNode, "handlers"):
                    for childNode in astNode.handlers:
                        result = parseModuleNode(childNode, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    newNodes.append(n)
                            else:
                                newNodes.append(result)
                if newNodes != []:
                    return newNodes
        return newNode

    # Initialization
    parsedString = _ast.parse(moduleText)
    moduleNodeTree = []
    # List of globals for testing for duplicates
    globalsList = []
    # Parse the nodes recursively
    for node in _ast.iter_child_nodes(parsedString):
        result = parseModuleNode(node, 0)
        if result != None:
            if isinstance(result, list):
                for n in result:
                    moduleNodeTree.append(n)
            else:
                moduleNodeTree.append(result)
    # Sort the node list
    moduleNodeTree = sorted(moduleNodeTree, key=lambda x: x.name)
    # Return the resulting tree
    return moduleNodeTree

if __name__ == "__main__":
    import sys
    app = _QtWidgets.QApplication(sys.argv)
    editor = PythonModuleInfo(r'E:\python\Writer-master\writer.py')
    editor.createModuleTree()
    editor.show()
    # editor.setText(open(r'E:\python\Writer-master\writer.py').read())
    # import pprint
    # for node in parsePythonModule(open(r'E:\python\Writer-master\writer.py', 'r').read()):
    #     print (node.name, node.line_number, node.type, node.children, node.level)

    app.exec_()