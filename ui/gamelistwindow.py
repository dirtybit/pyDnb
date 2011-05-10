from PyQt4.QtCore import pyqtSlot, pyqtSignal, qDebug
from PyQt4.QtGui import QMainWindow, QTableWidgetItem, QHeaderView
from ui_gamelistwindow import Ui_GameListWindow
from exitdialog import ExitDialog
from creategamedialog import CreateGameDialog
from Msgs import *
from sys import exit
from cPickle import dumps, loads

class GameListWindow(QMainWindow, Ui_GameListWindow):
    def __init__(self):
        """
        
        Arguments:
        - `self`:
        """
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.socket = None
        self.games = None

    def update_game_list(self):
        """
        """
        qDebug(str(len(self.games)) + ' games retrieved from server')
        print self.games
        self.gameTable.verticalHeader().setVisible(False)
        self.gameTable.horizontalHeader().resizeSections(QHeaderView.Fixed)
        self.gameTable.setRowCount(len(self.games))
        self.gameTable.setColumnCount(4)
        i = 0
        for game in self.games:
            self.gameTable.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.gameTable.setItem(i, 1, QTableWidgetItem('Game ' + str(game['i'])))
            self.gameTable.setItem(i, 2, QTableWidgetItem(str(game['n'])))
            self.gameTable.setItem(i, 3, QTableWidgetItem(str(game['cap'])))
            self.gameTable.verticalHeader().resizeSection(i, 18)
            i += 1
        print self.gameTable.currentRow()

    def closeEvent(self, event):
        """
        """
        #### TODO: exit game properly
        
        dialog = ExitDialog()
        if dialog.exec_():
            event.accept()
            msg = dict()
            msg['head'] = DELPLAYER
            msg['body'] = None
            self.socket.writeData(dumps(msg))
        else:
            event.ignore()

    # Signals
    join_successful = pyqtSignal('QTcpSocket')
    create_successful = pyqtSignal('QTcpSocket')    

    # Slots
    @pyqtSlot('QTcpSocket')
    def initialize(self, sock):
        """
        """
        self.socket = sock
        self.create_dialog = CreateGameDialog()
        self.refresh()
        self.connect()
        self.show()
    
    @pyqtSlot()
    def received(self):
        """
        """
        msg = self.socket.readData(4096)
        msg = loads(msg)
        print 'Msg:', msg
        head = msg['head']
        body = msg['body']

        if head == GAME_LIST:
            self.games = body
            self.update_game_list()
        elif head == SCREATE:
            qDebug('Game created')
            self.socket.readyRead.disconnect(self.received)
            self.create_successful.emit(self.socket)            
        elif head == SJOIN:
            qDebug('Join successful')
            self.socket.readyRead.disconnect(self.received)
            self.join_successful.emit(self.socket)
        else:
            pdbg(body)

    @pyqtSlot()
    def refresh(self):
        """
        """
        self.statusBar.clearMessage()        
        msg = dict()
        msg['head'] = GAME_LIST
        msg['body'] = None
        msg = dumps(msg)
        self.socket.writeData(msg)
        qDebug('Game list requested from server')

    @pyqtSlot(int)
    def create(self, n=6):
        """
        """
        self.statusBar.clearMessage()
        msg = dict()
        msg['head'] = CREATE
        msg['body'] = 6
        msg = dumps(msg)
        self.socket.writeData(msg)
        qDebug('Game create requested with n:' + str(n))
        
    @pyqtSlot()
    def join(self):
        """
        """
        row = self.gameTable.currentRow()

        if row == -1 or row >= len(self.games):
            self.statusBar.showMessage('You should select a game to join!')
        else:
            self.statusBar.clearMessage()            
            msg = dict()
            msg['head'] = JOIN
            msg['body'] = self.games[row]['i']                    # rowdaki oyun indexi
            msg = dumps(msg)
            self.socket.writeData(msg)
            qDebug('Join requested with index: ' + str(self.games[row]['i']))

    @pyqtSlot()
    def bas(self):
        """
        """
        print self.gameTable.currentRow()

    # Connections
    def connect(self):
        """
        """
        self.socket.readyRead.connect(self.received)
        self.createButton.clicked.connect(self.create)        
        # self.createButton.clicked.connect(self.create_dialog.show)
        # self.create_dialog.value_entered.connect(self.create)
        self.joinButton.clicked.connect(self.join)
        self.refreshButton.clicked.connect(self.refresh)
        self.exitButton.clicked.connect(self.close)
        self.gameTable.itemSelectionChanged.connect(self.bas)
