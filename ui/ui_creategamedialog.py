# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui_files/creategamedialog.ui'
#
# Created: Sat May  7 00:00:08 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CreateGameDialog(object):
    def setupUi(self, CreateGameDialog):
        CreateGameDialog.setObjectName(_fromUtf8("CreateGameDialog"))
        CreateGameDialog.resize(184, 73)
        self.widget = QtGui.QWidget(CreateGameDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 164, 55))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(18, 13, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dotNumberSpin = QtGui.QSpinBox(self.widget)
        self.dotNumberSpin.setObjectName(_fromUtf8("dotNumberSpin"))
        self.horizontalLayout.addWidget(self.dotNumberSpin)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CreateGameDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CreateGameDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CreateGameDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateGameDialog)

    def retranslateUi(self, CreateGameDialog):
        CreateGameDialog.setWindowTitle(QtGui.QApplication.translate("CreateGameDialog", "Create Game", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CreateGameDialog", "Enter dot number", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CreateGameDialog = QtGui.QDialog()
    ui = Ui_CreateGameDialog()
    ui.setupUi(CreateGameDialog)
    CreateGameDialog.show()
    sys.exit(app.exec_())

