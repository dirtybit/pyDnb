from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QDialog
from ui_creategamedialog import Ui_CreateGameDialog

class CreateGameDialog(QDialog, Ui_CreateGameDialog):
    def __init__(self):
        """
        
        Arguments:
        - `self`:
        """
        QDialog.__init__(self)
        self.setupUi(self)

    # Signals
    value_entered = pyqtSignal(int)

    # Slots
    @pyqtSlot()
    def accept(self):
        """
        """
        self.value_entered.emit(self.dotNumberSpin.value())
        super(CreateGameDialog, self).accept()
    
    @pyqtSlot()
    def reject(self):
        """
        """
        super(CreateGameDialog, self).reject()
    
    # Connections
