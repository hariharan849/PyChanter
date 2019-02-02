import sys as _sys
_sys.path.append(r'E:\development')

import os as _os
from PyQt5 import (
    QtWidgets as _QtWidgets,
    QtGui as _QtGui,
    QtCore as _QtCore
    )
from pyChanter import constants as _constants
from pyChanter import utils as _utils

class Directory(object):
    """
    Object for holding directory/file information when building directory trees
    """
    item = None
    directories = None
    files = None

    def __init__(self, inputItem):
        """Initialization"""
        self.item = inputItem
        self.directories = {}
        self.files = {}

    def addDirectory(self, dirName, dirItem):
        """
        Adds directory to the current item
        """
        # Create a new instance of Directory class using the __class__ dunder method
        newDirectory = self.__class__(dirItem)
        # Add the new directory to the dictionary
        self.directories[dirName] = newDirectory
        # Add the new directory item to the parent(self)
        self.item.appendRow(dirItem)
        # Return the directory object reference
        return newDirectory

    def addFile(self, fileName, fileItem):
        """
        Adds files to the current item
        """
        self.files[fileName] = fileItem
        # Add the new file item to the parent(self)
        self.item.appendRow(fileItem)


class DirectoryTree(_QtWidgets.QTreeView):
    """
    Directory tree to represent the current project
    """
    def __init__(self, parent=None):
        super(DirectoryTree, self).__init__(parent)
        self.folderIcon = _QtGui.QIcon(_constants.folderIcon)
        self.fileIcon = _QtGui.QIcon(_constants.fileIcon)

        # self.displayDirectory(r'E:\python\Pymakr\QScintilla')

    def _getDirModel(self, directory):
        """
        Creates directory modelf or the current directory
        """
        self.horizontalScrollbarAction(1)
        self.setSelectionBehavior(_QtWidgets.QAbstractItemView.SelectRows)
        treeModel = _QtGui.QStandardItemModel()
        treeModel.setHorizontalHeaderLabels(["FOUND FILES TREE"])
        self.header().hide()
        self._cleanModel()
        self.setModel(treeModel)
        self.setUniformRowHeights(True)
        self._setFontSettings(10)

        # Directory item
        itemDirectory = _QtGui.QStandardItem(
            "BASE DIRECTORY: {:s}".format(directory.replace("\\", "/"))
        )
        itemDirectory.setEditable(False)
        treeModel.appendRow(itemDirectory)
        return treeModel

    def _cleanModel(self):
        """
        Sets model to none
        """
        if self.model() is None:
            return
        self.model().setParent(None)
        self.setModel(None)

    def _setFontSettings(self, fontSize=10):
        """
        Sets default font as courier
        """
        newFont = _QtGui.QFont('Courier', fontSize)
        # Set the new font
        self.setFont(newFont)
        
    def _addItemsToTree(self, treeModel, directory, dirItems):
        if dirItems == []:
            noFilesFound = _QtGui.QStandardItem("No items found")
            noFilesFound.setEditable(False)
            # noFilesFound.setIcon(self.node_icon_nothing)
            # noFilesFound.setForeground(label_brush)
            noFilesFound.setFont(10)
            treeModel.appendRow([])
        else:
            # Set the UNIX file format to the directory
            directory = directory.replace("\\", "/")
            """Adding the files"""
            # label_brush = data.QBrush(
            #     data.QColor(data.theme.Font.Python.SingleQuotedString[1])
            # )
            labelFont = _QtGui.QFont(
                "Courier", 10, _QtGui.QFont.Bold
            )
            # item_brush = data.QBrush(
            #     data.QColor(data.theme.Font.Python.Default[1])
            # )
            itemFont = _QtGui.QFont("Courier", 10)
            # Create the base directory item that will hold all of the found files
            itemBaseDirectory = _QtGui.QStandardItem(directory)
            itemBaseDirectory.setEditable(False)
            # itemBaseDirectory.setForeground(label_brush)
            itemBaseDirectory.setFont(labelFont)
            itemBaseDirectory.setIcon(self.folderIcon)
            # Add an indicating attribute that shows the item is a directory.
            # It's a python object, attributes can be added dynamically!
            itemBaseDirectory.is_base = True
            itemBaseDirectory.fullPath = directory
            # Create the base directory object that will hold everything else
            baseDirectory = Directory(itemBaseDirectory)
            # Create the files that will be added last directly to the base directory
            baseFiles = {}
            # Sort the the item list so that all of the directories are before the files
            sortedItems = self._sortItemList(dirItems, directory)
            # Loop through the files while creating the directory tree
            for itemWithPath in sortedItems:
                if _os.path.isfile(itemWithPath):
                    file = itemWithPath.replace(directory, "")
                    fileName = _os.path.basename(file)
                    directoryName  = _os.path.dirname(file)
                    #Strip the first "/" from the files directory
                    if directoryName.startswith("/"):
                        directoryName = directoryName[1:]
                    #Initialize the file item
                    itemFile = _QtGui.QStandardItem(fileName)
                    itemFile.setEditable(False)
                    # itemFile.setForeground(item_brush)
                    itemFile.setFont(itemFont)
                    # file_type = functions.get_file_type(fileName)
                    itemFile.setIcon(_QtGui.QIcon(_utils.getFileTypeLogo(fileName)))
                    #Add an atribute that will hold the full file name to the QStandartItem.
                    #It's a python object, attributes can be added dynamically!
                    itemFile.fullPath = itemWithPath
                    #Check if the file is in the base directory
                    if directoryName == "":
                        #Store the file item for adding to the bottom of the tree
                        baseFiles[fileName] = itemFile
                    else:
                        #Check the previous file items directory structure
                        parsedDirectoryList = directoryName.split("/")
                        #Create the new directories
                        currentDirectory = baseDirectory
                        for dir in parsedDirectoryList:
                            #Check if the current loop directory already exists
                            if dir in currentDirectory.directories:
                                currentDirectory = currentDirectory.directories[dir]
                        #Add the file to the directory
                        currentDirectory.addFile(fileName, itemFile)
                else:
                    directoryName  = itemWithPath.replace(directory, "")
                    #Strip the first "/" from the files directory
                    if directoryName.startswith("/"):
                        directoryName = directoryName[1:]
                    #Check the previous file items directory structure
                    parsedDirectoryList = directoryName.split("/")
                    #Create the new directories
                    currentDirectory = baseDirectory
                    for dir in parsedDirectoryList:
                        #Check if the current loop directory already exists
                        if dir in currentDirectory.directories:
                            currentDirectory = currentDirectory.directories[dir]
                        else:
                            #Create the new directory item
                            itemNewDirectory = _QtGui.QStandardItem(dir)
                            itemNewDirectory.setEditable(False)
                            itemNewDirectory.setIcon(self.folderIcon)
                            # itemNewDirectory.setForeground(item_brush)
                            itemNewDirectory.setFont(itemFont)
                            #Add an indicating attribute that shows the item is a directory.
                            #It's a python object, attributes can be added dynamically!
                            itemNewDirectory.is_dir = True
                            itemNewDirectory.fullPath = itemWithPath
                            currentDirectory = currentDirectory.addDirectory(
                                dir,
                                itemNewDirectory
                            )
            # Add the base level files from the stored dictionary, first sort them
            for file_key in sorted(baseFiles, key=str.lower):
                baseDirectory.addFile(file_key, baseFiles[file_key])
            treeModel.appendRow(itemBaseDirectory)
            # Expand the base directory item
            self.expand(itemBaseDirectory.index())
            # Resize the header so the horizontal scrollbar will have the correct width
            self._resizeHorizontalScrollbar()

    def _sortItemList(self, items, directory):
        """
        Sorts directories and files
        """
        sortedDirectories = []
        sortedFiles = []
        for item in items:
            dir = _os.path.dirname(item)
            if (not dir in sortedDirectories):
                sortedDirectories.append(dir)
            if _os.path.isfile(item):
                sortedFiles.append(item)
        # Remove the base directory from the directory list, it is not needed
        if directory in sortedDirectories:
            sortedDirectories.remove(directory)
        # Sort the two lists case insensitively
        sortedDirectories.sort(key=str.lower)
        sortedFiles.sort(key=str.lower)
        # Combine the file and directory lists
        sortedItems = sortedDirectories + sortedFiles
        return sortedItems

    def displayDirectory(self, directory):
        """
        Displays directory tree.
        """
        treeModel = self._getDirModel(directory)
        # Initialize the list that will hold both the directories and files
        dirItems = []
        for item in _os.walk(directory):
            baseDirectory, subDir, files = item
            for dir in subDir:
                dirItems.append(_os.path.join(baseDirectory, dir).replace("\\", "/"))
            for file in files:
                dirItems.append(_os.path.join(baseDirectory, file).replace("\\", "/"))
        # Add the items to the treeview
        self._addItemsToTree(treeModel, directory, dirItems)


    def _resizeHorizontalScrollbar(self):
        """
        Resize the header so the horizontal scrollbar will have the correct width
        """
        for i in range(self.model().rowCount()):
            self.resizeColumnToContents(i)


if __name__ == '__main__':
    app = _QtWidgets.QApplication(_sys.argv)

    widget = DirectoryTree()
    widget.displayDirectory(r'E:\python\Pymakr\QScintilla')
    widget.show()

    app.exec_()