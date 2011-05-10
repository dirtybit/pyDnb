from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QDialog
from ui_exitdialog import Ui_ExitDialog

class ExitDialog(QDialog, Ui_ExitDialog):
    def __init__(self):
        """
        
        Arguments:
        - `self`:
        """
        QDialog.__init__(self)
        self.setupUi(self)

    # Signals
    exit_confirmed = pyqtSignal()

    # Slots
    @pyqtSlot()
    def accept(self):
        """
        """
        super(ExitDialog, self).accept()
    
    @pyqtSlot()
    def reject(self):
        """
        """
        super(ExitDialog, self).reject()
    
    # Connections
