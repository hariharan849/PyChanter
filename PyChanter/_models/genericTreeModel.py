"""
Generic tree model and node to be inherited and modified by other tree model
"""

from PyQt5 import QtCore as _QtCore


class GenericNode(object):
    
    def __init__(self, name, parent=None):
        """
        Generic Node for generic tree model
        :param name(Str Object): Name of the tree node()
        :param parent(Node Object): Parent of the current Node
        """
        self._name = name
        self._children = []
        self._parent = parent
        
        if parent is not None:
            parent.addChild(self)

    def addChild(self, child):
        """
        Appends child for the current Parent
        :param child: Child Node object
        """
        self._children.append(child)

    def insertChild(self, position, child):
        """
        Inserts child Node object in the specific Position
        :param position(int object): Postion to insert
        :param child(Node Object): Child Node object
        """
        if position < 0 or position > len(self._children):
            return False
        
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        """
        Removes Child from the specific position
        :param position(int object): Postion to delete
        :return: Boolean
        """
        if position < 0 or position > len(self._children):
            return False
        
        child = self._children.pop(position)
        child._parent = None
        return True

    def name(self):
        """
        Returns Name of the current Node
        :return: Str
        """
        return self._name

    def setName(self, name):
        """
        Sets name to the current Node
        :param name(str object): Name of the node
        """
        self._name = name

    def child(self, row):
        """
        Returns child at the specific row
        :param row(int Object): Row of the node to fetch
        :return: Node
        """
        return self._children[row]
    
    def childCount(self):
        """
        Returns length of the child
        :return: int
        """
        return len(self._children)

    def parent(self):
        """
        Returns Parent of the current node
        :return: Node
        """
        return self._parent
    
    def row(self):
        """
        Returns Child node
        :return: Node or None
        """
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tabLevel=-1):
        """
        Prints the tree
        :param tabLevel(int Object): tablevel for displaying
        """
        output     = ""
        tabLevel += 1
        
        for i in range(tabLevel):
            output += "\t"
        
        output += "|------" + self._name + "\n"
        
        for child in self._children:
            output += child.log(tabLevel)
        
        tabLevel -= 1
        output += "\n"
        
        return output

    def __repr__(self):
        return self.log()


class GenericTreeModel(_QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        """
        Generic Tree Model to inherit and modify for QTreeView
        :param root(Node object): Root Node of the model
        :param parent: Parent of the model
        """
        super(GenericTreeModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        """
        Returns the child count of the current Node
        :param parent: QModelIndex
        :return: int
        """
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()

    def columnCount(self, parent):
        """
        Returns ColumnCount of the Model
        :param parent: QModelIndex
        :return: int
        """
        return 1

    def data(self, index, role):
        """
        Returns Data to display for various rows
        :param index: QModelIndex
        :param role: Role to act(DisplayRole)
        :return: Str to display
        """
        if not index.isValid():
            return None

        node = index.internalPointer()
        if role == _QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return node.name()

    def setData(self, index, value, role=_QtCore.Qt.EditRole):
        """
        Sets Data based on role passed
        :param index: QModelIndex
        :param value: Str
        :param role: Role to act
        """
        if index.isValid():
            if role == _QtCore.Qt.EditRole:
                node = index.internalPointer()
                node.setName(value)
                return True
        return False

    def headerData(self, section, orientation, role):
        """
        Returns Header data to display in column
        """
        if role == _QtCore.Qt.DisplayRole:
            return ""
            if section == 0:
                return "Find In Files"

    def flags(self, index):
        """
        Returns Flags for the data
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def parent(self, index):
        """
        Return the parent of the node with the given QModelIndex
        """
        node = self.getNode(index)
        parentNode = node.parent()
        
        if parentNode == self._rootNode:
            return _QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        """
        Return a QModelIndex that corresponds to the given row, column and parent node
        """
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return _QtCore.QModelIndex()

    def getNode(self, index):
        """
        Returns Node of the Current Index
        """
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode

    def insertRows(self, position, rows, parent=_QtCore.QModelIndex()):
        """
        Inserts Node at the specified Position
        """
        parentNode = self.getNode(parent)
        success = False

        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=_QtCore.QModelIndex()):
        """
        Removes Rows at the specified position
        """
        parentNode = self.getNode(parent)
        success = False

        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)
        self.endRemoveRows()
        
        return success
