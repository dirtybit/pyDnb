from PyQt4.QtGui import QDialog
from ui_waitingdialog import Ui_WaitingDialog

class WaitingDialog(QDialog, Ui_WaitingDialog):
    def __init__(self, parent=None):
        """
        
        Arguments:
        - `self`:
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
