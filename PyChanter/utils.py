"""
Utils for PyChanter application
"""
import os as _os
import ast as _ast
import collections as _collections
from PyChanter import constants as _constants


def getFileTypeLogo(fileWithPath):
    """
    Get file extension and return file type as string
    :param fileWithPath: Path of the file
    :return(str): Logo paths
    """
    #Initialize it as unknown and change it in the if statement
    fileIcon = "file_logo.png"
    #Split the file and path
    path, file = _os.path.split(fileWithPath)
    #Split file name and extension
    fileName, fileExtension = _os.path.splitext(file)
    if fileExtension.lower() in _constants.pythonExtensions:
        fileIcon = 'python_logo.png'
    elif fileExtension.lower() == _constants.xmlExtensions:
        fileIcon = 'xml_logo.png'
    elif fileExtension.lower() == _constants.jsonExtensions:
        fileIcon = 'json_logo.png'
    elif fileExtension.lower() == _constants.yamlExtensions:
        fileIcon = 'yaml_logo.png'
    return _os.path.join(_constants.iconsFolder, fileIcon)


def findTextInDirectory(searchText, searchDir, caseSensitive=False):
    """
    Search for the specified text in files in the specified directory and return a file list and
    lines where the text was found at.
    :param searchText(str): Name of the search text
    :param searchDir(str): Name of the directory
    :param caseSensitive(boolean): Flag for case sensitive
    :return: Dict
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
            if validateTextFile(completeFilePath) != None:
                # On windows, the function "os.path.join(root, file)" line gives a combination of "/" and "\\",
                # which looks weird but works. The replace was added to have things consistent in the return file list.
                completeFilePath = completeFilePath.replace("\\", "/")
                textFileList.append(completeFilePath)
    # Search for the text in found files
    returnFileDict = _collections.defaultdict(list)
    for file in textFileList:
        try:
            fileLines = readFileToList(file)
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
                    returnFileDict[file].append((i, fileLines[i]))
        except:
            continue
    # Return the generated list
    return returnFileDict

def validateTextFile(fileWithPath):
    """
    Test if a file is a plain text file and can be read
    :param fileWithPath(str): File Path
    :return:
    """
    try:
        file = open(fileWithPath, "r", encoding=locale.getpreferredencoding(), errors="strict")
        # Read only a couple of lines in the file
        for line in itertools.islice(file, 10):
            line = line
        file.readlines()
        # Close the file handle
        file.close()
        # Return the systems preferred encoding
        return locale.getpreferredencoding()
    except:
        validencodings = ["utf-8", "ascii", "utf-16", "utf-32", "iso-8859-1", "latin-1"]
        for currentEncoding in validencodings:
            try:
                file = open(fileWithPath, "r", encoding=currentEncoding, errors="strict")
                # Read only a couple of lines in the file
                for line in itertools.islice(file, 10):
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

def readFileToList(filePath):
    """
        Read contents of a text file to a list
        :param fileWithPath(str): File Path
        :return:
    """
    text = readFileToString(filePath)
    if text != None:
        return text.split("\n")
    else:
        return None

def readFileToString(filePath):
    """
        Read contents of a text file to a single string
        :param fileWithPath(str): File Path
        :return:
    """
    # Test if a file is in binary format
    binaryText = testBinaryFile(filePath)
    if binaryText != None:
        return
    else:
        # File is not binary, loop through encodings to find the correct one.
        # Try the default Ex.Co. encoding UTF-8 first
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

def testBinaryFile(filePath):
    """
        Test if a file is in binary format
        :param fileWithPath(str): File Path
        :return:
    """
    file = open(filePath, "rb")
    #Read only a couple of lines in the file
    binaryText = None
    for line in itertools.islice(file, 20):
        if b"\x00" in line:
            #Return to the beginning of the binary file
            file.seek(0)
            #Read the file in one step
            binaryText = file.read()
            break
    file.close()
    #Return the result
    return binaryText

def getParsedPythonNode(pythonText):
    """
    Parse the text and return nodes as a nested tree.
    """
    class NodeDetails(object):
        def __init__(self, name, objectType, lineNo, levelIndex):
            self.name = name
            self.objectType = objectType
            self.lineNo = lineNo
            self.levelIndex = levelIndex
            self.children = []

    # Main parsing function
    def convertParsedNodeToNodeDetails(astNode, level, parentNode=None):
        nonlocal globalsInformation
        nonlocal nodeTree
        newNode = None
        if isinstance(astNode, _ast.ClassDef):
            newNode = NodeDetails(
                astNode.name,
                "class",
                astNode.lineno,
                level
            )
            for childNode in astNode.body:
                result = convertParsedNodeToNodeDetails(childNode, level + 1, newNode)
                if result != None:
                    if isinstance(result, list):
                        for n in result:
                            newNode.children.append(n)
                    else:
                        newNode.children.append(result)
            newNode.children = sorted(newNode.children, key=lambda x: x.name)
        elif isinstance(astNode, _ast.FunctionDef):
            newNode = NodeDetails(
                astNode.name,
                "function",
                astNode.lineno,
                level
            )
            for childNode in astNode.body:
                result = convertParsedNodeToNodeDetails(childNode, level + 1, newNode)
                if result != None:
                    if isinstance(result, list):
                        for n in result:
                            newNode.children.append(n)
                    else:
                        newNode.children.append(result)
            newNode.children = sorted(newNode.children, key=lambda x: x.name)
        elif isinstance(astNode, _ast.Import):
            newNode = NodeDetails(
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
                    if not (name in globalsInformation):
                        newNodes.append(
                            NodeDetails(
                                name,
                                "global_variable",
                                astNode.lineno,
                                level
                            )
                        )
                        globalsInformation.append(name)
            return newNodes
        elif isinstance(astNode, _ast.Global):
            # Globals can be nested somewhere deep in the AST, so they
            # are appended directly into the non-local nodeTree list
            for name in astNode.names:
                if not (name in globalsInformation):
                    nodeTree.append(
                        NodeDetails(
                            name,
                            "global_variable",
                            astNode.lineno,
                            level
                        )
                    )
                    globalsInformation.append(name)
        else:
            if parentNode != None and hasattr(astNode, "body"):
                for childNode in astNode.body:
                    result = convertParsedNodeToNodeDetails(childNode, level + 1, parentNode)
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
                        result = convertParsedNodeToNodeDetails(childNode, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    newNodes.append(n)
                            else:
                                newNodes.append(result)
                if hasattr(astNode, "orelse"):
                    for childNode in astNode.orelse:
                        result = convertParsedNodeToNodeDetails(childNode, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    newNodes.append(n)
                            else:
                                newNodes.append(result)
                if hasattr(astNode, "finalbody"):
                    for childNode in astNode.finalbody:
                        result = convertParsedNodeToNodeDetails(childNode, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    newNodes.append(n)
                            else:
                                newNodes.append(result)
                if hasattr(astNode, "handlers"):
                    for childNode in astNode.handlers:
                        result = convertParsedNodeToNodeDetails(childNode, level + 1, None)
                        if result != None:
                            if isinstance(result, list):
                                for n in result:
                                    newNodes.append(n)
                            else:
                                newNodes.append(result)
                if newNodes != []:
                    return newNodes
        return newNode

    pythonParsedObject = _ast.parse(pythonText)
    nodeTree = []
    # List of globals for testing for duplicates
    globalsInformation = []
    # Parse the nodes recursively
    for node in _ast.iter_child_nodes(pythonParsedObject):
        result = convertParsedNodeToNodeDetails(node, 0)
        if result != None:
            if isinstance(result, list):
                for n in result:
                    nodeTree.append(n)
            else:
                nodeTree.append(result)
    # Sort the node list
        nodeTree = sorted(nodeTree, key=lambda x: x.name)
    return nodeTree

if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # editor = NodeDisplay()
    # editor.show()
    # editor.setText(open(sys.argv[0]).read())
    import pprint
    for node in getParsedPythonNode(open(r'E:\development\pyChanterMay25\launchApplication.py', 'r').read()):
        print (node.name, node.lineNo, node.objectType, node.children, node.levelIndex)

    # app.exec_()