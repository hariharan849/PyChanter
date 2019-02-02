"""
IPython console widget
"""
from qtconsole.rich_ipython_widget import RichIPythonWidget
from qtconsole.inprocess import QtInProcessKernelManager


class EmbedIPython(RichIPythonWidget):

    def __init__(self, parent=None):
        super(RichIPythonWidget, self).__init__(parent)
        self.kernel_manager = QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel = self.kernel_manager.kernel
        self.kernel.gui = 'qt4'
        # self.kernel.shell.push(kwarg)
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()
        self.kernel.shell.run_cell('%pylab qt')

if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    console = EmbedIPython()
    console.show()
    sys.exit(app.exec_())