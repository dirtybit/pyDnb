'''
Created on Apr 17, 2011

@author: sertac
'''

from cPickle import dumps, loads
from threading import Lock, Semaphore, Thread

from Msgs import *

class DnbGame(Thread):
    '''
    classdocs
    '''
    def __init__(self,server, n, player):
        """
        """
        self.server = server
        self.players = list()
        self.players.append(player)
        self.turn = 0
        self.score = [0, 0]
        self.names = []
        self.n = n
        self.counter = (n - 1)**2
        self.started = False
        self.ready = Semaphore(0)
        self.cap = 'Available'
        self.join_control = Lock()
        self.delta_lines = None
        self.delta_marks = None
        self.last_turn_owner = 0
        self.finished = False
        Thread.__init__(self)
        self.start()

    def add_player(self, player):
        if not self.started:
            self.players.append(player)
            if len(self.players) == 2:
                self.started = True
                self.cap = 'Full!'
            return True
        else:
            return False

    def leave(self):
        """
        """
        ### oyuncusu kalmayan oyunu serverdan sil, oyun sayisindan dus
        pass

    def killhim(self, i):
        ### RC0 (done)
        with self.server.player_control:
            self.server.players -= 2
        ### RC1 (done)must be implemented in a way to support multigame
        with self.server.game_control:
            index = self.server.games.index(self)
            self.server.games[index] = None
            
            self.server.games_number -= 1
        ### End RC1
        self.players[i].send(dumps(None))
        pdbg('\tPlayers and game deleted (ACK)')
                ### End RC0

    def run(self):
        self.ready.acquire()
        self.ready.acquire()
        #map(lambda player: player.send(GAMESTART), self.players)

        while True:
            player0_msg = dict()
            player1_msg = dict()
            player0_msg['lines'] = player1_msg['lines'] = self.delta_lines
            player0_msg['marks'] = player1_msg['marks'] = self.delta_marks
            player0_msg['finished'] = player1_msg['finished'] = self.finished
            player0_msg['turn'] = 'o' if self.turn else 'y'
            player1_msg['turn'] = 'y' if self.turn else 'o'
            player0_msg['score'] = {'y': self.score[0], 'o': self.score[1]}
            player1_msg['score'] = {'y': self.score[1], 'o': self.score[0]}
            player0_msg['owner'] = 'o' if self.last_turn_owner else 'y'
            player1_msg['owner'] = 'y' if self.last_turn_owner else 'o'

            try:
                self.players[0].send(dumps(player0_msg))
            except:
                self.killhim(1)
                break
            
            try:    
                self.players[1].send(dumps(player1_msg))
            except:
                self.killhim(0)
                break 

            if self.finished:
                self.killhim(0)
                break
                
            msg0 = self.players[0].recv(SIZE)
            msg1 = self.players[1].recv(SIZE)
            try:
                msg0 = loads(msg0)
            except:
                self.killhim(1)
                break

            try:
                msg1 = loads(msg1)
            except:
                self.killhim(0)
                break

            if msg0[0] == TURN_RECVD:    # player 1 moved
                msg = msg1[1]
                self.score[1] = msg['score']['y']
                self.score[0] = msg['score']['o']
                self.delta_lines = msg['lines']
                self.delta_marks = msg['marks']
                self.turn = 1 if msg['turn'] == 'y' else 0
                self.last_turn_owner = 1
            elif msg1[0] == TURN_RECVD:                        # player 0 moved
                msg = msg0[1]
                self.score[0] = msg['score']['y']
                self.score[1] = msg['score']['o']
                self.delta_lines = msg['lines']
                self.delta_marks = msg['marks']
                self.turn = 0 if msg['turn'] == 'y' else 1
                self.last_turn_owner = 0
            else:
                # remove players remove game from server RC for server game
                pdbg('End game request')
                ### RC0 (done)
                with self.server.player_control:
                    self.server.players -= 2
                ### RC1 (done)must be implemented in a way to support multigame
                with self.server.game_control:
		    index = self.server.games.index(self)
                    self.server.games_list[index] = None
                    self.server.games[index] = None
                ### End RC1
                self.players[0].send(SDELP)
                self.players[1].send(SDELP)
                pdbg('\tPlayers and game deleted (ACK)')
                ### End RC0
                break

            pdbg('Turn message received ' + str(msg))

            if self.score[0] + self.score[1] == self.counter:
                self.finished = True

    def play(self):
        self.ready.release()

