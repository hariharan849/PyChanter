import os as _os
import constants as _constants

def getFileTypeLogo(fileWithPath):
    """Get file extension and return file type as string"""
    #Initialize it as unknown and change it in the if statement
    fileIcon = "file_logo.png"
    #Split the file and path
    path, file = _os.path.split(fileWithPath)
    #Split file name and extension
    fileName, fileExtension   = _os.path.splitext(file)
    if fileExtension.lower() in _constants.pythonExtensions:
        fileIcon = 'python_logo.png'
    elif fileExtension.lower() == _constants.xmlExtensions:
        fileIcon = 'xml_logo.png'
    elif fileExtension.lower() == _constants.jsonExtensions:
        fileIcon = 'json_logo.png'
    elif fileExtension.lower() == _constants.yamlExtensions:
        fileIcon = 'yaml_logo.png'
    return _os.path.join(_constants.iconsFolder, fileIcon)
