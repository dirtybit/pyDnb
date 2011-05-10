# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui_files/waitingDialog.ui'
#
# Created: Fri May  6 23:59:50 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_WaitingDialog(object):
    def setupUi(self, WaitingDialog):
        WaitingDialog.setObjectName(_fromUtf8("WaitingDialog"))
        WaitingDialog.resize(206, 48)
        self.widget = QtGui.QWidget(WaitingDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 188, 31))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.busyBar = QtGui.QProgressBar(self.widget)
        self.busyBar.setMaximum(0)
        self.busyBar.setProperty(_fromUtf8("value"), 8548)
        self.busyBar.setObjectName(_fromUtf8("busyBar"))
        self.horizontalLayout.addWidget(self.busyBar)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WaitingDialog)
        QtCore.QMetaObject.connectSlotsByName(WaitingDialog)

    def retranslateUi(self, WaitingDialog):
        WaitingDialog.setWindowTitle(QtGui.QApplication.translate("WaitingDialog", "Waiting", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("WaitingDialog", "Waiting for an opponent to start game", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    WaitingDialog = QtGui.QDialog()
    ui = Ui_WaitingDialog()
    ui.setupUi(WaitingDialog)
    WaitingDialog.show()
    sys.exit(app.exec_())

