import resource_rc

from PyQt4 import QtGui
from PyQt4 import QtCore
from sys import argv
app = QtGui.QApplication([argv])

item = QtGui.QLabel('sertac')
item.setPixmap(QtGui.QPixmap(':/board/y'))
item.show()

app.exec_()
                         
