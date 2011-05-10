#!/usr/bin/python

from sys import argv
from PyQt4.QtGui import QApplication
from ui.connectwindow import ConnectWindow
from ui.gamelistwindow import GameListWindow
from ui.board import *

def main(args):
    app = QApplication(args)
    connect_window = ConnectWindow()
    game_list_window = GameListWindow()
    board = Board()

    connect_window.conn_success.connect(game_list_window.initialize)
    game_list_window.create_successful.connect(board.after_create)
    game_list_window.join_successful.connect(board.after_join)
    board.ui_ready.connect(game_list_window.hide)
    
    connect_window.show()
    app.exec_()


if __name__ == "__main__":
    main(argv)
