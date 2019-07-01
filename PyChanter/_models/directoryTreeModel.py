"""
Directory tree model to display directory Information
"""

from . import genericTreeModel as _genericTreeModel


class DirectoryTreeModel(_genericTreeModel.GenericTreeModel):
    def headerData(self, section, orientation, role):
        """
        Returns Header data to display in column
        """
        if role == _QtCore.Qt.DisplayRole:
            if section == 0:
                return "Find In Files"
        super(DirectoryTreeModel, self).headerData(section, orientation, role)

    def flags(self, index):
        """
        Returns Flags for the data
        """
        return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
