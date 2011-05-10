# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/gview.ui'
#
# Created: Sat May  7 23:53:45 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(700, 745)
        Form.setGeometry(QtCore.QRect(0, 0, 700, 745))
        Form.setMinimumSize(QtCore.QSize(700, 745))
        Form.setMaximumSize(QtCore.QSize(700, 745))
        self.graphicsView = QtGui.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 700, 730))
        self.graphicsView.setMinimumSize(QtCore.QSize(700, 730))
        self.graphicsView.setMaximumSize(QtCore.QSize(700, 730))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

import resource_rc
