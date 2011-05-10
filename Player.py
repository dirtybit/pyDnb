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

    def handle_request(self, request):
        """
        """
        head = request['head']
        body = request['body']

        response = dict()
        if head == GAME_LIST:
            pdbg('Game list requested')
            
            response['head'] = GAME_LIST

            with self.server.game_control:
                self.server.games_list = list()
                i = 0
                for game in self.server.games:
                    if game:
                        d = {}
                        d['i'] = i
                        d['n'] = game.n
                        d['cap'] = game.cap
                        self.server.games_list.append(d)
                    i += 1
                    
                
                for game in self.server.games_list:
                    pdbg('\tGame #%(i)d, Size: %(n)d, Cap: %(cap)s' % game)

            response['body'] = self.server.games_list
            self.sock.send(dumps(response))
            
        elif head == UIREADY:
            pdbg('User Interface ready for client')
            self.game.play()
            
            return False
        elif head == DELPLAYER:
            pdbg('Delete player request')
            response['head'] = SDELP
            response['body'] = None
            ### RC0 (done)
            with self.server.player_control:
                self.server.players -= 1
            self.sock.send(dumps(response))
            pdbg('\tPlayer deleted (ACK sent)')
            ### End RC0

            return False
        elif head == CREATE:
            n = body
            pdbg('Create op. requested with n: %d' % n)
            if not self.game:
                ### RC1 (done)
                with self.server.game_control:
                    if self.server.games_number >= self.server.max_game:
                        response['head'] = UCREATE
                        response['body'] = 'Game cannot be created. Max game limit reached'
                        pdbg('\tGame cannot be created. Max game limit reached' + str(self.server.games_number))
                    else:
                        response['head'] = SCREATE
                        response['body'] = n
                        self.game = DnbGame(self.server, n, self)
                        self.server.add_game(self.game)
                        self.server.games_number += 1
                        pdbg('\tGame created')
                ### End RC1
            else:
                response['head'] = UCREATE
                response['body'] = 'Game cannot be created'
                pdbg('\tGame cannot be created')
            self.sock.send(dumps(response))
        elif head == JOIN:
            index = body
            pdbg('Join op. requested for Game #%d' % index)
            if not self.game:
                self.game = self.server.games[index]
                ### RC2 (done)
                with self.game.join_control:
                    res = self.game.add_player(self)
                if not res:
                    response['head'] = UJOIN
                    response['body'] = 'Join unsuccessful for Game#%d' % index
                    pdbg('\tJoin unsuccessful for Game#%d' % index)
                ### End RC2
                else:
                    response['head'] = SJOIN
                    response['body'] = self.game.n
                    pdbg('\tJoin successful for Game#%d' % index)
            else:
                response['head'] = UJOIN
                response['body'] = 'Join unsuccessful for Game#%d' % index
                pdbg('\tJoin unsuccessful for Game#%d' % index)
            self.sock.send(dumps(response))
        return True
    
    def run(self):
        """
        """
        i=1
        while True:
            raw_msg = self.sock.recv(SIZE)
            print 'Turn:', i
            i+=1
            if raw_msg:
                request = loads(raw_msg)
                print request
                if not self.handle_request(request):
                    break            
            else:
                pdbg('Connection closed')
                break

