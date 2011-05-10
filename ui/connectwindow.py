from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMainWindow
from PyQt4.QtNetwork import QTcpSocket
from ui_connectwindow import Ui_ConnectWindow
from exitdialog import ExitDialog
from cPickle import loads
from Msgs import *

class ConnectWindow(QMainWindow, Ui_ConnectWindow):
    def __init__(self):
        """
        
        Arguments:
        - `self`:
        """
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.socket = QTcpSocket()
        self.connect()

    # Signals
    conn_success = pyqtSignal('QTcpSocket')
    exit_signal = pyqtSignal()

    # Slots
    @pyqtSlot()
    def connect_server(self):
        """
        """
        self.statusBar.clearMessage()
        host = self.serverLine.text().trimmed()
        port = self.portLine.text().trimmed()

        if host and port:
            self.socket.connectToHost(host, int(port))
        else:
            self.statusBar.showMessage('Enter valid a server address and port!')
        
    @pyqtSlot()
    def on_success(self):
        """
        """
        if self.socket.waitForReadyRead(10000):
            msg = self.socket.readData(1024)
            msg = loads(msg)
            if msg['head'] == CONN_SUCC:
                self.statusBar.showMessage('Connection established')
                self.conn_success.emit(self.socket)
                self.hide()
            else:
                self.statusBar.showMessage('Server is full!')
                self.socket.disconnectFromHost()
        else:
            self.on_error()

    @pyqtSlot()        
    def on_error(self):
        self.statusBar.showMessage('Connection cannot be established!')

    def closeEvent(self, event):
        """
        """
        dialog = ExitDialog()
        if dialog.exec_():
            event.accept()
        else:
            event.ignore()

    # Connections
    def connect(self):
        """
        """
        self.connectButton.clicked.connect(self.connect_server)
        self.exitButton.clicked.connect(self.close)
        self.socket.error.connect(self.on_error)
        self.socket.connected.connect(self.on_success)
