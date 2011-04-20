'''
Created on Apr 17, 2011

@author: sertac
'''
from cPickle import dumps, loads
from threading import Thread

from DnbGame import DnbGame
from Msgs import *


class Player(Thread):
    '''
    classdocs
    '''
    def __init__(self, server, sock, addr):
        """
        """
        self.addr = addr
        self.sock = sock
        self.server = server
        self.game = None
        Thread.__init__(self)

    def send(self, msg):
        '''
        '''
        self.sock.send(msg)

    def recv(self, size):
        '''
        '''
        return self.sock.recv(size)

    def run(self):
        """
        """
        while True:
            raw_msg = self.sock.recv(SIZE)
            if raw_msg:
                msg = loads(raw_msg)
                header = msg[0]
            else:
                header = None

            if header == GAME_LIST:
                pdbg('Game list requested')
                with self.server.game_control:
                    for game in self.server.games_list:
                        pdbg('\tGame #%(i)d, Size: %(n)d, Cap: %(cap)s' % game)

                self.sock.send(dumps(self.server.games_list))
            elif header == UIREADY:
                pdbg('User Interface ready for client')
                self.game.play()
                break
            elif header == DELPLAYER:
                pdbg('Delete player request')
                ### RC0 (done)
                if self.game:
                    self.game.leave()
                with self.server.player_control:
                    self.server.players -= 1
                self.sock.send(SDELP)
                pdbg('\tPlayer deleted (ACK)')
                break
                ### End RC0
            elif header == CREATE:
                n = msg[1]
                pdbg('Create op. requested with n: %d' % n)
                if not self.game:
                    ### RC1 (done)
                    with self.server.game_control:
                        if len(self.server.games) >= self.server.max_game:
                            self.sock.send(UCREATE)
                            pdbg('\tGame cannot be created. Max game limit reached')
                        else:
                            self.game = DnbGame(self.server, n, self)
                            self.server.add_game(self.game)
                            self.sock.send(SCREATE)
                            pdbg('\tGame created')
                    ### End RC1
                else:
                    self.sock.send(UCREATE)
                    pdbg('\tGame cannot be created')
            elif header == JOIN:
                index = msg[1]
                pdbg('Join op. requested for Game #%d' % index)
                if not self.game:
                    self.game = self.server.games[index]
                    ### RC2 (done)
                    with self.game.join_control:
                        res = self.game.add_player(self)
                    if not res:
                        self.sock.send(UJOIN)
                        pdbg('\tJoin unsuccessful for Game#%d' % index)
                    ### End RC2
                    self.sock.send(SJOIN)
                    pdbg('\tJoin successful for Game#%d' % index)
                else:
                    self.sock.send(UJOIN)
                    pdbg('\tJoin unsuccessful for Game#%d' % index)
            elif header:
                self.sock.send(CONN_FAIL)
                pdbg('Connection failed')
            else:
                pdbg('Connection closed')
                break


