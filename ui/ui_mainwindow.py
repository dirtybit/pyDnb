# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui_files/mainwindow.ui'
#
# Created: Fri May  6 23:58:06 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(523, 570)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1, 0, 521, 531))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gameTableView = QtGui.QTableView(self.layoutWidget)
        self.gameTableView.setObjectName(_fromUtf8("gameTableView"))
        self.verticalLayout.addWidget(self.gameTableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.createButton = QtGui.QPushButton(self.layoutWidget)
        self.createButton.setObjectName(_fromUtf8("createButton"))
        self.horizontalLayout.addWidget(self.createButton)
        self.joinButton = QtGui.QPushButton(self.layoutWidget)
        self.joinButton.setObjectName(_fromUtf8("joinButton"))
        self.horizontalLayout.addWidget(self.joinButton)
        self.refreshButton = QtGui.QPushButton(self.layoutWidget)
        self.refreshButton.setObjectName(_fromUtf8("refreshButton"))
        self.horizontalLayout.addWidget(self.refreshButton)
        spacerItem = QtGui.QSpacerItem(167, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.exitButton = QtGui.QPushButton(self.layoutWidget)
        self.exitButton.setObjectName(_fromUtf8("exitButton"))
        self.horizontalLayout.addWidget(self.exitButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 523, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuGame = QtGui.QMenu(self.menubar)
        self.menuGame.setObjectName(_fromUtf8("menuGame"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.refreshAction = QtGui.QAction(MainWindow)
        self.refreshAction.setObjectName(_fromUtf8("refreshAction"))
        self.createAction = QtGui.QAction(MainWindow)
        self.createAction.setObjectName(_fromUtf8("createAction"))
        self.joinAction = QtGui.QAction(MainWindow)
        self.joinAction.setObjectName(_fromUtf8("joinAction"))
        self.exitAction = QtGui.QAction(MainWindow)
        self.exitAction.setObjectName(_fromUtf8("exitAction"))
        self.helpAction = QtGui.QAction(MainWindow)
        self.helpAction.setObjectName(_fromUtf8("helpAction"))
        self.aboutAction = QtGui.QAction(MainWindow)
        self.aboutAction.setObjectName(_fromUtf8("aboutAction"))
        self.menuGame.addAction(self.refreshAction)
        self.menuGame.addAction(self.createAction)
        self.menuGame.addAction(self.joinAction)
        self.menuGame.addSeparator()
        self.menuGame.addAction(self.exitAction)
        self.menuHelp.addAction(self.helpAction)
        self.menuHelp.addAction(self.aboutAction)
        self.menubar.addAction(self.menuGame.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Dots and Boxes", None, QtGui.QApplication.UnicodeUTF8))
        self.createButton.setText(QtGui.QApplication.translate("MainWindow", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.joinButton.setText(QtGui.QApplication.translate("MainWindow", "Join", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGame.setTitle(QtGui.QApplication.translate("MainWindow", "Game", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshAction.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.createAction.setText(QtGui.QApplication.translate("MainWindow", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.joinAction.setText(QtGui.QApplication.translate("MainWindow", "Join", None, QtGui.QApplication.UnicodeUTF8))
        self.exitAction.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.helpAction.setText(QtGui.QApplication.translate("MainWindow", "Game Help", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutAction.setText(QtGui.QApplication.translate("MainWindow", "About Dots and Boxes", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

