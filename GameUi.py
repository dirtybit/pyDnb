'''
Created on Apr 17, 2011

@author: sertac
'''
import curses
import os
from cPickle import loads, dumps
from Msgs import *

class GameUi:
    '''
    classdocs
    '''

    def __init__(self, sock, scrn, n):
        '''
        Constructor
        '''
        self.sock = sock
        self.board = GameUi.Board(scrn, n)

    def init_game(self):
        """
        """
        self.board.init_board()
        self.board.draw_board()
        msg = dumps([UIREADY])
        self.sock.send(msg)
        raw_turnmsg = self.sock.recv(SIZE)    # turn message requested
        turn = loads(raw_turnmsg)

        while True:
            if turn['owner'] == 'o':
                self.board.update(turn)

            msg = list()

            if turn['turn'] == 'y' and not turn['finished']:
                updates = self.board.move_prompt()
                msg.append(MOVE)
                msg.append(updates)
            elif not turn['finished']:
                self.board.move_waiting()
                msg.append(TURN_RECVD)
                self.board.turn = 'o'

            self.board.draw_board()

            if turn['finished']:
                break
            self.sock.send(dumps(msg))

            raw_turnmsg = self.sock.recv(SIZE)    # turn message requested
            try:
                turn = loads(raw_turnmsg)
            except:
                self.sock.send(dumps([DELPLAYER]))
                msg = self.sock.recv(SIZE)
                if msg == SDELP:
                    self.sock.close()
                os.system('clear')
                sys.exit(0)

        self.sock.send(dumps([DELPLAYER]))
        msg = self.sock.recv(SIZE)
        if msg == SDELP:
            self.sock.close()
        self.board.end_game()


    class GameException(Exception):
        '''
        classdocs
        '''
        def __init__(self, value):
            self.msg = value

        def __str__(self):
            return repr(self.msg)

    class Board:
        """
        """

        def __init__(self, scrn, n):
            """
            """
            self.title = 'pyDnb - Dots and Boxes Game'
            self.n = int(n);
            self.turn = 0
            self.score = dict()
            self.scrn = scrn
            self.vpad = 3
            self.hpad = 5
            self.vspace = 4
            self.hspace = 7
            self.vlines = [[False for j in range(self.n)] for i in range(self.n - 1)]
            self.hlines = [[False for j in range(self.n - 1)] for i in range(self.n)]
            self.marks = dict()
            self.marks['y'] = 'Y'
            self.marks['o'] = 'O'
            self.score['y'] = 0
            self.score['o'] = 0
            self.finished = False

        def init_board(self):
            self.scrn.erase()

            self._draw_ruler()
            self._draw_dots()

        def update(self, conf):
            """
            Arguments:
            - `self`:
            - `conf`:
            """
            if conf['lines']:
                self._check_point(conf['lines'])
            if conf['marks']:
                self.mark_location(conf['marks'])
            self.turn = conf['turn']
            self.score['y'] = conf['score']['y']
            self.score['o'] = conf['score']['o']
            self.draw_board()

        def draw_board(self):
            self._draw_lines()
            self._print_score()

        def end_game(self):
            y = self.vpad * 3  + self.n * self.vspace + 3
            x = self.hpad
            self.scrn.addstr(y, x, "%30c" % ' ')
            self.show_msg('Game is over. Press \'q\' to exit.')
            self.finished = True
            self._print_score()

            while True:
                ch = self.scrn.getkey()
                if ch == 'q':
                    os.system('clear')
                    break

        def _draw_ruler(self):
            ###############
            h, w = self.scrn.getmaxyx()
            oldx, oldy = self.scrn.getyx()
            self.scrn.addstr(1, w/2 - len(self.title), self.title)
            self.scrn.move(oldx, oldy)

            for i in range(self.n):
                # horizontal ruler ' letters
                x = i * self.hspace + self.hspace + self.hpad - 1
                self.scrn.addstr(self.vpad, x, chr(ord('a')+i))
                # vertical ruler ' numbers
                frmt = "%%%dd" % self.hpad
                y = (i + 1) * self.vspace + self.vpad
                self.scrn.addstr(y, 0, frmt % i)

            self.scrn.refresh()

        def _draw_dots(self):
            frmt = "%%%dc" % self.hspace
            for i in range(self.n):
                for j in range(self.n):
                    y = (i + 1) * self.vspace + self.vpad
                    x = j * self.hspace + self.hpad
                    self.scrn.addstr(y, x, frmt % '*' )
            self.scrn.refresh()

        def _draw_lines(self):
            """
            """
            i, j = 0, 0

            while i < self.n:
                j = 0
                while j < self.n - 1:
                    if self.hlines[i][j]:
                        self._draw_hline(j, i)
                    if self.vlines[j][i]:
                        self._draw_vline(i, j)
                    j += 1
                i += 1

        def _draw_vline(self, x, y):
            oldy, oldx = self.scrn.getyx()

            _x = self.hspace * (x + 1) + self.hpad - 1
            _y = (y + 1) * self.vspace + self.vpad + 1
            self.scrn.vline(_y, _x, curses.ACS_VLINE, self.vspace - 1)

            self.scrn.move(oldy, oldx)

        def _draw_hline(self, x, y):
            oldy, oldx = self.scrn.getyx()

            _x = self.hspace * (x + 1) + self.hpad
            _y = (y + 1) * self.vspace + self.vpad
            self.scrn.hline(_y, _x, curses.ACS_HLINE, self.hspace - 1)

            self.scrn.move(oldy, oldx)

        def _print_score(self):   ### should be updated
            """
            """
            y = self.vpad * 3  + self.n * self.vspace
            x = self.hpad
            self.scrn.addstr(y, x, "You: " + str(self.score['y']) + '%20s' % ' ')
            self.scrn.addstr(y+1, x, "Opponent: " + str(self.score['o']))
            self.scrn.addstr(y+2, x, ("Winner: " + ("You" if self.score['y'] > self.score['o'] else "Opponent") if self.finished else "Turn: " + (('You %20s' % ' ') if self.turn == 'y' else "Opponent")))
            self.scrn.refresh()

        def move_prompt(self):
            """
            """
            while True:
                y = self.vpad * 3  + self.n * self.vspace + 3
                x = self.hpad
                msg = "Enter move: "
                self.scrn.addstr(y, x, msg)
                self.scrn.addstr(y, x+len(msg), "%20c" % " ")
                self.scrn.move(y,x+len(msg))
                move = self.scrn.getstr()
                try:
                    self._check_move(move)
                    update = self._do_move(move)
                    update['score'] = dict()
                    update['score']['y'] = self.score['y']
                    update['score']['o'] = self.score['o']
                    return update
                except GameUi.GameException as ge:
                    self.show_error(ge.msg)
                    continue

        def move_waiting(self):
            """
            """
            y = self.vpad * 3  + self.n * self.vspace + 3
            x = self.hpad
            msg = "Waiting opponent to move "
            self.scrn.addstr(y, x, msg)
            self.scrn.addstr(y, x+len(msg), "%20c" % " ")
            self.scrn.move(y,x+len(msg))

        def _check_move(self, move):
            if len(move) != 4:
                raise GameUi.GameException('Wrong move!')

            dot1, dot2 = self._get_dots(move)

            if self._check_dot(dot1) != True or self._check_dot(dot2) != True:
                raise GameUi.GameException('Wrong move!')

            if self._is_horizontal(move) and abs(dot1[1]-dot2[1]) != 1:
                raise GameUi.GameException('Wrong move!')

            if self._is_vertical(move) and abs(dot1[0]-dot2[0]) != 1:
                raise GameUi.GameException('Wrong move!')

            if not self._is_vertical(move) and not self._is_horizontal(move):
                raise GameUi.GameException('Wrong move!')

            if self._line_exist(move):
                raise GameUi.GameException('Wrong move!')

        def _get_dots(self, move):
            y1, x1 = ord(move[0]) - ord('0'), ord(move[1]) - ord('a')
            y2, x2 = ord(move[2]) - ord('0'), ord(move[3]) - ord('a')
            dot1 = (y1, x1)
            dot2 = (y2, x2)

            return (dot1, dot2)

        def _line_exist(self, move):
            dot1, dot2 = self._get_dots(move)

            if self._is_vertical(move):
                return self.vlines[min(dot1[0], dot2[0])][dot1[1]]
            else:
                return self.hlines[dot1[0]][min(dot1[1], dot2[1])]

        def _is_vertical(self, move):
            dot1, dot2 = self._get_dots(move)
            return dot1[1] == dot2[1]

        def _is_horizontal(self, move):
            dot1, dot2 = self._get_dots(move)
            return dot1[0] == dot2[0]

        def _check_dot(self, dot):
            """
            """
            return (dot[0] < self.n and dot[0] >= 0) and (dot[1] < self.n and dot[1] >= 0)

        def _do_move(self, move):
            """
            """
            update = dict()
            update['lines'] = move
            update['marks'] = None
            update['turn'] = 'o'
            test = self._check_point(move)
            if test > 0:
                # karenin icini oyuncu adi ile isaretle
                current_mark = self._mark_squares(move, test)
                update['marks'] = current_mark
                update['turn'] = 'y'

            return update

        def _check_point(self, move):
            """
            """
            dot1, dot2 = self._get_dots(move)

            if self._is_vertical(move):
                self.vlines[min(dot1[0], dot2[0])][dot1[1]] = True
                row, col = min(dot1[0], dot2[0]), dot1[1]
                return self._hsquare_test(row, col)
            else:
                self.hlines[dot1[0]][min(dot1[1], dot2[1])] = True
                row, col = dot1[0], min(dot1[1], dot2[1])
                return self._vsquare_test(row, col)

        def _hsquare_test(self, row, col):
            sval = 0
            if not self._left_border(row, col) and (self.vlines[row][col-1] and self.hlines[row][col - 1] and self.hlines[row + 1][col - 1]):
                sval += 4
            if not self._right_border(row, col) and (self.vlines[row][col + 1] and self.hlines[row][col] and self.hlines[row + 1][col]):
                sval += 5

            return sval

        def _vsquare_test(self, row, col):
            sval = 0
            if not self._top_border(row, col) and (self.hlines[row - 1][col] and self.vlines[row - 1][col] and self.vlines[row - 1][col + 1]):
                sval += 1
            if not self._bottom_border(row, col) and (self.hlines[row + 1][col] and self.vlines[row][col] and self.vlines[row][col + 1]):
                sval += 2

            return sval

        def _left_border(self, row, col):
            return col == 0

        def _right_border(self, row, col):
            return col == self.n - 1

        def _top_border(self, row, col):
            return row == 0

        def _bottom_border(self, row, col):
            return row == self.n - 1

        def _mark_squares(self, move, testval):
            current_marks = dict()
            if testval > 5:
                self.score['y'] += 2
                self._mark_location(current_marks, move, 5)
                self._mark_location(current_marks, move, 4)
            elif testval > 4:
                self.score['y'] += 1
                self._mark_location(current_marks, move, 5)
            elif testval > 3:
                self.score['y'] += 1
                self._mark_location(current_marks, move, 4)
            elif testval > 2:
                self.score['y'] += 2
                self._mark_location(current_marks, move, 2)
                self._mark_location(current_marks, move, 1)
            elif testval > 1:
                self.score['y'] += 1
                self._mark_location(current_marks, move, 2)
            elif testval > 0:
                self.score['y'] += 1
                self._mark_location(current_marks, move, 1)
            else:
                pass

            return current_marks

        def mark_location(self, locs):
            for (_x, _y), mark in locs.items():
                oldy, oldx = self.scrn.getyx()
                self.scrn.move(_y, _x)
                self.scrn.addstr('O')
                self.scrn.move(oldy, oldx)

        def _mark_location(self, dict, move, val):
            y1, x1 = ord(move[0]) - ord('0'), ord(move[1]) - ord('a')
            y2, x2 = ord(move[2]) - ord('0'), ord(move[3]) - ord('a')

            if val == 1:
                x = min(x1, x2)
                y = y1 - 1
            elif val == 2:
                x = min(x1, x2)
                y = y1
            elif val == 4:
                x = x1 - 1
                y = min(y1, y2)
            elif val == 5:
                x = x1
                y = min(y1, y2)

            oldy, oldx = self.scrn.getyx()
            _x = self.hspace/2 + self.hspace * (x + 1) + self.hpad - 1
            _y = self.vspace/2 + (y + 1) * self.vspace + self.vpad
            self.scrn.move(_y, _x)
            self.scrn.addstr(self.marks[self.turn])
            self.scrn.move(oldy, oldx)
            dict[(_x, _y)] = self.marks[self.turn]

        def show_msg(self, msg):
            """
            """
            oldy, oldx = self.scrn.getyx()
            y = self.vpad * 3  + self.n * self.vspace + 4
            x = self.hpad
            self.scrn.addstr(y, x, msg)
            self.scrn.move(oldy, oldx)

        def show_error(self, msg):
            """
            """
            oldy, oldx = self.scrn.getyx()
            y = self.vpad * 3  + self.n * self.vspace + 4
            x = self.hpad
            self.scrn.attron(curses.color_pair(1))
            self.scrn.addstr(y, x, "*Error!* " + msg)
            self.scrn.attroff(curses.color_pair(1))
            self.scrn.move(oldy, oldx)
