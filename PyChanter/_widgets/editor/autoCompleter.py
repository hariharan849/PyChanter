"""
Jedi functionality to fetch module names from python index and pre loads module in thread
"""

import os as _os
import jedi as _jedi
import requests as _requests
import bs4 as _bs4
import pip as _pip
from PyQt5 import QtCore as _QtCore
from PyChanter import constants as _constants


class AutoCompleter(_QtCore.QThread):
    """
    Jedi settings for the application
    """
    def __init__(self):
        super(AutoCompleter, self).__init__()
        cacheDirectory = _os.path.join(_constants.currentFolder, '.cache', 'jedi')
        if not _os.path.exists(cacheDirectory):
            _os.makedirs(cacheDirectory)
        _jedi.settings.cache_directory = cacheDirectory
        _jedi.settings.add_bracket_after_function = False
        _jedi.settings.no_completion_duplicates = True
        _jedi.settings.fast_parser = True
        _jedi.settings.use_filesystem_cache = True
        _jedi.settings.call_signatures_validity = 3.0
        _jedi.evaluate.dynamic = True
        _jedi.evaluate.recursion.recursion_limit = 15
        _jedi.evaluate.recursion.total_function_execution_limit = 200
        _jedi.evaluate.recursion.per_function_execution_limit = 6
        _jedi.evaluate.recursion.per_function_recursion_limit = 2

    def run(self):
        url = "https://docs.python.org/3/py-modindex.html"
        try:
            moduleHtml = _requests.get(url)
        except _requests.exceptions.ConnectionError:
            return
        if moduleHtml.status_code != 200:
            return
        soup = _bs4.BeautifulSoup(moduleHtml.text)
        codeIndex = soup.find_all("code")
        moduleNames = [moduleName.text for moduleName in codeIndex if not moduleName.text.startswith('__')]
        _jedi.preload_module(moduleNames)
