'''
Created on Apr 17, 2011

@author: sertac
'''
from socket import socket, AF_INET, SOCK_STREAM
from threading import Lock
from cPickle import loads, dumps
from Msgs import *
from Player import Player

class GameServer:
    '''
    classdocs
    '''
    def __init__(self, n=1,host='', port=9080):
        self.host = host
        self.port = port
        self.games_list = []
        self.games = []
        self.games_number = 0
        self.max_game = n
        self.game_lock = Lock()
        self.player_control = Lock()
        self.game_control = Lock()
        self.players = 0

    def add_game(self, game):
        d = {}
        d['i'] = len(self.games_list)
        d['n'] = game.n
        d['cap'] = game.cap
        self.games_list.append(d)
        self.games.append(game)

    def start_server(self):
        """
        """
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

        ack = dict()
        ack['body'] = None

        while True:
            conn, addr = self.sock.accept()
            ### Player:RC0 (done)
            with self.player_control:
                if self.players < 2*self.max_game:
                    self.players += 1
                    p = Player(self, conn, addr)
                    ack['head'] = CONN_SUCC
                    p.start()
                else:
                    ack['head'] = CONN_FAIL
                conn.send(dumps(ack))
            ### End Player:RC0

