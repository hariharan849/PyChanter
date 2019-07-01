import os as _os

currentFolder = _os.path.join(_os.path.dirname(__file__))
resourcesFolder = _os.path.join(currentFolder, 'resources')

#StyleSheet
styleSheetFolder = _os.path.join(resourcesFolder, 'styleSheet', 'QTDark1.stylesheet')

# Icons
iconsFolder = _os.path.join(resourcesFolder, 'icons')
folderIcon = _os.path.join(iconsFolder, 'folder.png')
fileIcon = _os.path.join(iconsFolder, 'file.png')

# Extensions
pythonExtensions = ('.py', 'pyc')
jsonExtensions = 'json'
xmlExtensions = 'xml'
yamlExtensions = 'yaml'

# Font
defaultDirectoryFontSize = 10
defaultFontSize = 14

#Untitled format
UNTITLED = "untitled_{0}"