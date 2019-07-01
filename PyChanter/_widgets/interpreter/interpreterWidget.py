
import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication

from pyqtconsole.console import PythonConsole


class InterpreterWidget(PythonConsole):
    def __init__(self, parent=None):
        super(InterpreterWidget, self).__init__(parent)
        self.eval_in_thread()

    def runFile(self, fileName):
        with open(fileName) as fb:
            inputCodeObject = compile(fb.read(), filename=fileName, mode='exec')
            self.interpreter.runcode(inputCodeObject)

if __name__ == '__main__':
    app = QApplication([])
    console = InterpreterWidget()
    console.show()

    sys.exit(app.exec_())