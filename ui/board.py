#!/usr/bin/python

from PyQt4 import QtGui
from PyQt4 import QtCore
from ui_board import Ui_Form
from itertools import product
from waitingdialog import WaitingDialog
from exitdialog import ExitDialog
from Msgs import *
from cPickle import dumps, loads

class Board(QtGui.QMainWindow, Ui_Form):

    vline_xposes = [116.0, 205.0, 294.0, 381.0, 477.0, 573.0]
    vline_yposes = [133.0, 215.0, 294.0, 375.0, 462.0]
    vline_poses = list(product(vline_xposes, vline_yposes))
    
    hline_xposes = [132.0, 223.0, 308.0, 401.0, 494.0]
    hline_yposes = [125.0, 204.0, 284.0, 363.0, 456.0, 534.0]
    hline_poses = list(product(hline_xposes, hline_yposes))

    mark_xposes = [160.0, 252.0, 344.0, 437.0, 529.0]
    mark_yposes = [167.0, 247.0, 326.0, 406.0, 495.0]
    mark_poses = list(product(mark_xposes, mark_yposes))
    
    def __init__(self):
        """
        """
        QtGui.QMainWindow.__init__(self)
        self.line_map = dict()
        self.lines = 60 * [False]
        self.line_items = 60 * [None]
        self.socket = None
        self.n = 6
        self.t = 0
        
        self.turn = 'y'
        self.score = {'y':0, 'o':0}
        self.dline = None
        self.dmark = None
        self.avail = False
        
        self.setupUi(self)
        self.statusBar = QtGui.QStatusBar(self)
        self.statusBar.setObjectName('statusBar')
        self.setStatusBar(self.statusBar)
        self.scene = DnbScene(0, 0, 700, 730)
        self.scene.installEventFilter(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMouseDoubleClick and not self.avail:
            print 'You can\'t play'
            return True
        else:
            return QtGui.QMainWindow.eventFilter(self, obj, event)

        
    def closeEvent(self, event):
        """
        """
        #### TODO: exit game properly
        
        dialog = ExitDialog()
        if dialog.exec_():
            event.accept()
        else:
            event.ignore()

    def update_scoreboard(self):
        """
        """
        pass

    def add_line(self, line):
        """
        """
        self.line_items[line][0].setZValue(3)
        self.scene.removeItem(self.line_items[line][1])
        self.lines[line] = True

        #returns marks
        marks = list()

        if self.up_square(line):
            marks.append(self.mark_number(line-self.n+1))
        if self.down_square(line):
            marks.append(self.mark_number(line+self.n))
        if self.left_square(line):
            marks.append(self.mark_number(line))
        if self.right_square(line):
            marks.append(self.mark_number(line+1))

        return marks
    
    def add_marks_y(self, marks):
        """
        """
        # update score

        for mark in marks:
            x, y = Board.mark_poses[mark]
            pitem = QtGui.QGraphicsPixmapItem()
            pitem.setPos(x-15, y-15)
            pitem.setPixmap(QtGui.QPixmap(":/board/y"))
            pitem.setZValue(5)
            self.scene.addItem(pitem)

        self.score['y'] += len(marks)
    
    def add_marks_o(self, marks):
        """
        """
        # update score
        for mark in marks:
            x, y = Board.mark_poses[mark]
            pitem = QtGui.QGraphicsPixmapItem()
            pitem.setPos(x-15, y-15)
            pitem.setPixmap(QtGui.QPixmap(":/board/o"))
            pitem.setZValue(5)
            self.scene.addItem(pitem)

    def finish_game(self):
        """
        """
        turnMsg = 'You Win' if self.score['y'] > self.score['o'] else 'You Lost'
        scoreMsg = ('You: %d\tOpponent: %d\t\t' % (self.score['y'], self.score['o'])) + turnMsg
        self.statusBar.showMessage(scoreMsg)
        # close connection etc
        QtGui.QMessageBox.information(self, 'Game Over', turnMsg)
        exit(0)


    # Signals
    ui_ready = QtCore.pyqtSignal()
    exit_game = QtCore.pyqtSignal()

    # Slots
    @QtCore.pyqtSlot()
    def on_turn_recvd(self):
        """
        """
        msg = loads(self.socket.readData(4096))
        self.t += 1
        print '------------------------ Turn #' + str(self.t) + ' Started ------------------------'
        print 'Received turn message'
        print '   ', 'Message:', msg
        
        if msg:
            # Valid message
            line = msg['lines']
            marks = msg['marks']
            finished = msg['finished']
            owner = msg['owner']
            self.turn = msg['turn']
            self.score = msg['score']
            
            if owner != 'y':
                if line != None:
                    print 'Lines to be added:', line
                    self.add_line(line)
                if marks != [] and marks != None:
                    print 'Opponents marks:', marks
                    self.add_marks_o(marks)
                self.update_scoreboard()
                turnMsg = 'Your turn' if self.turn == 'y' else 'Opponent\'s turn'
                scoreMsg = ('You: %d\tOpponent: %d\t\t' % (self.score['y'], self.score['o'])) + turnMsg
                self.statusBar.showMessage(scoreMsg)

            if finished:
                self.finish_game()
            elif self.turn == 'y':
                self.avail = True
            else:
                self.avail = False
                amsg = list()
                amsg.append(TURN_RECVD)
                smsg = dumps(amsg)
                self.socket.writeData(smsg)
                print '------------------------- Turn #' + str(self.t) + ' Ended -------------------------'
        else:
            # Opponent quit unexpectedly
            QtGui.QMessageBox.critical(self, 'Game Over', 'Opponent has just quitted. Game over!', 'Exit Game')
            exit(0)
        

    
    @QtCore.pyqtSlot('QTcpSocket')
    def after_create(self, sock):
        """
        """
        self.init_board()
        self.socket = sock
        self.connect()
        dialog = WaitingDialog(self)
        self.socket.readyRead.connect(dialog.hide)
        self.show()
        self.ui_ready.emit()
        dialog.show()  # MODAL!!!
        pass # Opponent join
        self.show()
        msg = dict()
        msg['head'] = UIREADY
        msg['body'] = None
        msg = dumps(msg)
        self.socket.writeData(msg)
        self.socket.writeData('START')
        QtCore.qDebug('GUI ready notification sent')
        
    @QtCore.pyqtSlot('QTcpSocket')
    def after_join(self, sock):
        """
        """
        self.init_board()
        self.socket = sock
        self.connect()
        self.show()
        self.ui_ready.emit()
        msg = dict()
        msg['head'] = UIREADY
        msg['body'] = None
        msg = dumps(msg)
        self.socket.writeData(msg)
        self.socket.writeData('START')
        QtCore.qDebug('GUI ready notification sent')

    @QtCore.pyqtSlot('QPointF')
    def on_line_add(self, point, b=False):
        """
        """
        x, y = point.x(), point.y()
        line = self.line_map[(x, y)]
        
        if not self.lines[line]:
            self.avail = False
            marks = self.add_line(line)

            
            print 'Your move adds line:', line
            print 'Your marks:', marks
            self.add_marks_y(marks) # update score
            
            # send turn message
            msg = dict()
            msg['lines'] = line
            msg['marks'] = marks
            self.turn = msg['turn'] = 'y' if marks else 'o'
            msg['score'] = self.score

            turnMsg = 'Your turn' if self.turn == 'y' else 'Opponent\'s turn'
            scoreMsg = ('You: %d\tOpponent: %d\t\t' % (self.score['y'], self.score['o'])) + turnMsg
            self.statusBar.showMessage(scoreMsg)
            
            print '------------------------- Turn #' + str(self.t) + ' Ended -------------------------'
            smsg = [MOVE, msg]
            smsg = dumps(smsg)
            self.socket.writeData(smsg)

    # Connections
    def connect(self):
        """
        """
        self.socket.readyRead.connect(self.on_turn_recvd)
        self.scene.line_added.connect(self.on_line_add)

    # Test functions
    def is_horizontal(self, i):
        """
        """
        return (i % (2*self.n-1)) < self.n-1

    def is_vertical(self, i):
        """
        """
        return not self.is_horizontal(i)

    def right_border(self, i):
        """
        """
        if self.is_horizontal(i):
            return False
        else:
            return ((i+1) % (2*self.n-1)) == 0

    def left_border(self, i):
        """
        """
        return self.right_border(i+self.n-1)

    def top_border(self, i):
        """
        """
        return i >= 0 and i < self.n-1

    def bottom_border(self, i):
        """
        """
        return i > (2*self.n*(self.n-1))-self.n and i < 2*self.n*(self.n-1)

    def up_square(self, i):
        """
        """
        if self.top_border(i) or self.is_vertical(i):
            return False
        else:
            return self.lines[i-self.n] and self.lines[i+1-self.n] and self.lines[i-(2*self.n-1)]

    def down_square(self, i):
        """
        """
        if self.bottom_border(i) or self.is_vertical(i):
            return False
        else:
            return self.lines[i+self.n] and self.lines[i-1+self.n] and self.lines[i+(2*self.n-1)]
    
    def left_square(self, i):
        """
        """
        if self.left_border(i) or self.is_horizontal(i):
            return False
        else:
            return self.lines[i-self.n] and self.lines[i-1] and self.lines[i+self.n-1]

    def right_square(self, i):
        """
        """
        if self.right_border(i) or self.is_horizontal(i):
            return False
        else:
            return self.lines[i+self.n] and self.lines[i+1-self.n] and self.lines[i+1]

    def mark_number(self, r):
        c = 2*self.n-1
        a = r/c
        b = (r-self.n) % c
        return a + b*(self.n-1)
    
    def init_board(self):
        """
        """
        # Set background
        bgItem = QtGui.QGraphicsPixmapItem()
        bg = QtGui.QPixmap(":/board/bg")
        bgItem.setPixmap(bg)
        bgItem.setZValue(2)
        self.scene.addItem(bgItem)

        # Add horiontal lines and selection region as invisible
        i = 0
        j = 0
        for line_pos in Board.hline_poses:
            line_item = HLineItem(line_pos)
            line_item.setZValue(1)
            self.scene.addItem(line_item)
            self.line_map[line_pos] = j

            x, y = line_pos
            rect = HRectItem(x+5, y-5)
            rect.setZValue(0)
            self.scene.addItem(rect)
            self.line_items[j] = (line_item, rect)
            if j >= 55:
                i += 1
                j = i
            else:
                j += 11

        # Add vertical lines and selection region as invisible
        i = 5
        j = 5
        for line_pos in Board.vline_poses:
            line_item = VLineItem(line_pos)
            line_item.setZValue(1)
            self.scene.addItem(line_item)
            self.line_map[line_pos] = j

            x, y = line_pos
            rect = VRectItem(x-5, y+5)
            rect.setZValue(0)
            self.scene.addItem(rect)
            self.line_items[j] = (line_item, rect)            
            if j >= 49:
                i += 1
                j = i
            else:
                j += 11

class DnbScene(QtGui.QGraphicsScene):
    def __init__(self, *args):
        """
        """
        super(DnbScene, self).__init__(*args)

    def addItem(self, item):
        """
        """
        if isinstance(item, RectItem):
            item.obj.drawn.connect(self.remove_rect)
            item.obj.line_added.connect(self.line_added_slot)
        super(DnbScene, self).addItem(item)

    # Signals
    line_added = QtCore.pyqtSignal('QPointF', bool)
    
    # Slots
    @QtCore.pyqtSlot('QPointF')
    def line_added_slot(self, p):
        self.line_added.emit(p, True)
    
    @QtCore.pyqtSlot('QGraphicsPixmapItem')
    def remove_rect(self, ritem):
        """
        """
        pass #self.removeItem(ritem)

class RectObj(QtCore.QObject):
    def __init__(self):
        super(RectObj, self).__init__()

    def emit(self, pixmap, point):
        self.drawn.emit(pixmap)
        self.line_added.emit(point)

    # Signal
    drawn = QtCore.pyqtSignal('QGraphicsPixmapItem')
    line_added = QtCore.pyqtSignal('QPointF')
    
class RectItem(QtGui.QGraphicsPixmapItem):
    def __init__(self, x, y):
        super(RectItem, self).__init__()
        self.obj = RectObj()
        self.setPos(x, y)

    def mouseDoubleClickEvent(self, event):
        items = self.collidingItems()
        hline = items[1]
        hline.setZValue(3)
        self.obj.emit(self, hline.pos())

class VRectItem(RectItem):
    def __init__(self, x, y):
        super(VRectItem, self).__init__(x, y)
        self.setPixmap(QtGui.QPixmap(':/board/vrect'))

class HRectItem(RectItem):
    def __init__(self, x, y):
        super(HRectItem, self).__init__(x, y)
        self.setPixmap(QtGui.QPixmap(':/board/hrect'))

class LineItem(QtGui.QGraphicsPixmapItem):
    def __init__(self, pos):
        """
        """
        super(LineItem, self).__init__()
        self.setPos(pos[0], pos[1])

class HLineItem(LineItem):
    def __init__(self, pos):
        """
        """
        super(HLineItem, self).__init__(pos)
        self.setPixmap(QtGui.QPixmap(":/board/hline"))

class VLineItem(LineItem):
    def __init__(self, pos):
        """
        """
        super(VLineItem, self).__init__(pos)
        self.setPixmap(QtGui.QPixmap(":/board/vline"))
    
