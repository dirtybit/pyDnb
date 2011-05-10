from PyQt4.QtCore import QModelIndex, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QAbstractItemModel

class GameTableModel(QAbstractItemModel):
    """
    """
    
    def __init__(self, ):
        """
        """
        super(GameTableModel, self).__init__()

    def index(self, row, col, ind):
        """
        """
        return row

    def parent(self, child):
        """
        """
        return QModelIndex()

    def rowCount(self, parent = QModelIndex()):
        """
        
        Arguments:
        - `self`:
        - `parent`:
        """
        return None


        
        

