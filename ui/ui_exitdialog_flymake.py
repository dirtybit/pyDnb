# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui_files/exitdialog.ui'
#
# Created: Fri May  6 23:59:25 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ExitDialog(object):
    def setupUi(self, ExitDialog):
        ExitDialog.setObjectName(_fromUtf8("ExitDialog"))
        ExitDialog.resize(192, 67)
        self.buttonBox = QtGui.QDialogButtonBox(ExitDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 30, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(ExitDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 211, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(ExitDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExitDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExitDialog)

    def retranslateUi(self, ExitDialog):
        ExitDialog.setWindowTitle(QtGui.QApplication.translate("ExitDialog", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ExitDialog", "Are you sure to want to exit game?", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ExitDialog = QtGui.QDialog()
    ui = Ui_ExitDialog()
    ui.setupUi(ExitDialog)
    ExitDialog.show()
    sys.exit(app.exec_())

