# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui_files/connectwindow.ui'
#
# Created: Sat May  7 02:03:37 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ConnectWindow(object):
    def setupUi(self, ConnectWindow):
        ConnectWindow.setObjectName(_fromUtf8("ConnectWindow"))
        ConnectWindow.resize(176, 110)
        self.centralwidget = QtGui.QWidget(ConnectWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(11, 11, 158, 78))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.serverLine = QtGui.QLineEdit(self.widget)
        self.serverLine.setObjectName(_fromUtf8("serverLine"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.serverLine)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.portLine = QtGui.QLineEdit(self.widget)
        self.portLine.setObjectName(_fromUtf8("portLine"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.portLine)
        spacerItem = QtGui.QSpacerItem(36, 19, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(2, QtGui.QFormLayout.LabelRole, spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.connectButton = QtGui.QPushButton(self.widget)
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.horizontalLayout.addWidget(self.connectButton)
        self.exitButton = QtGui.QPushButton(self.widget)
        self.exitButton.setObjectName(_fromUtf8("exitButton"))
        self.horizontalLayout.addWidget(self.exitButton)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        ConnectWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(ConnectWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        ConnectWindow.setStatusBar(self.statusBar)

        self.retranslateUi(ConnectWindow)
        QtCore.QMetaObject.connectSlotsByName(ConnectWindow)

    def retranslateUi(self, ConnectWindow):
        ConnectWindow.setWindowTitle(QtGui.QApplication.translate("ConnectWindow", "Dots and Boxes", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ConnectWindow", "Server", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ConnectWindow", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.connectButton.setText(QtGui.QApplication.translate("ConnectWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("ConnectWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

