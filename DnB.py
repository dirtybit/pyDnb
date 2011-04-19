'''
Created on Mar 31, 2011

@author: sertac
'''
import curses
import os

class DnB:
    '''
    classdocs
    '''

    class GameException(Exception):
        '''
        classdocs
        '''
        def __init__(self, value):
            self.msg = value

        def __str__(self):
            return repr(self.msg)

    def __init__(self, n):
        '''
        Constructor
        '''
        self.n = int(n);
        self.turn = 0
        self.score = [0, 0]
        self.scrn = None
        self.vpad = 2
        self.hpad = 3
        self.vspace = 4
        self.hspace = 7
        self.vlines = [[False for j in range(self.n)] for i in range(self.n - 1)]
        self.hlines = [[False for j in range(self.n - 1)] for i in range(self.n)]
        self.counter = (self.n - 1) ** 2
        self.marks = ['A', 'B']

    def init_game(self):
        self.scrn = curses.initscr()
        #curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)

        self._draw_ruler()
        self._draw_dots()
        
        while self.counter:
            self._draw_lines()
            self._print_score()
            self._move_prompt()

        #curses.noecho()
        #self._draw_ruler()
        #self._draw_dots()
        self._draw_lines()
        self._print_score()
        y = self.vpad * 3  + self.n * self.vspace + 3
        x = self.hpad
        self.scrn.addstr(y, x, "%30c" % ' ')
        self._show_msg('Game is over. Press \'q\' to exit.')

        while True:
            ch = self.scrn.getkey()
            if ch == 'q':
                os.system('clear')
                break

    def _draw_ruler(self):
        for i in range(self.n):
            # horizontal ruler ' letters
            x = i * self.hspace + self.hspace + self.hpad -1
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

    def _print_score(self):
        """
        """
        y = self.vpad * 3  + self.n * self.vspace
        x = self.hpad
        self.scrn.addstr(y, x, "Player A: " + str(self.score[0]))
        self.scrn.addstr(y+1, x, "Player B: " + str(self.score[1]))
        self.scrn.addstr(y+2, x, ("Winner: " + ("B" if self.score[1] > self.score[0] else "A") if self.counter == 0 else "Turn: " + ("B" if self.turn else "A")))
        self.scrn.refresh()

    def _move_prompt(self):
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
                self._do_move(move)
                self.turn = self.turn ^ 1
                break
            except DnB.GameException as ge:
                self._show_error(ge.msg)
                continue

    def _check_move(self, move):
        dot1, dot2 = self._get_dots(move)

        if self._check_dot(dot1) != True or self._check_dot(dot2) != True:
            raise DnB.GameException('Wrong move!')

        if self._is_horizontal(move) and abs(dot1[1]-dot2[1]) != 1:
            raise DnB.GameException('Wrong move!')

        if self._is_vertical(move) and abs(dot1[0]-dot2[0]) != 1:
            raise DnB.GameException('Wrong move!')

        if not self._is_vertical(move) and not self._is_horizontal(move):
            raise DnB.GameException('Wrong move!')

        if self._line_exist(move):
            raise DnB.GameException('Wrong move!')

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
        test = self._check_point(move)
        if test > 0:
            # karenin icini oyuncu adi ile isaretle
            self._mark_squares(move, test)
            self.turn = self.turn ^ 1
        self._show_msg("Last Move: " + move + "%15c" % ' ')

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
        if testval > 5:
            self.score[self.turn] += 2
            self.counter -= 2
            self._mark_location(move, 5)
            self._mark_location(move, 4)
        elif testval > 4:
            self.score[self.turn] += 1
            self.counter -= 1
            self._mark_location(move, 5)
        elif testval > 3:
            self.score[self.turn] += 1
            self.counter -= 1
            self._mark_location(move, 4)
        elif testval > 2:
            self.score[self.turn] += 2
            self.counter -= 2
            self._mark_location(move, 2)
            self._mark_location(move, 1)
        elif testval > 1:
            self.score[self.turn] += 1
            self.counter -= 1
            self._mark_location(move, 2)
        elif testval > 0:
            self.score[self.turn] += 1
            self.counter -= 1
            self._mark_location(move, 1)
        else:
            pass

    def _mark_location(self, move, val):
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

    def _show_msg(self, msg):
        """
        """
        oldy, oldx = self.scrn.getyx()
        y = self.vpad * 3  + self.n * self.vspace + 4
        x = self.hpad
        self.scrn.addstr(y, x, msg)
        self.scrn.move(oldy, oldx)

    def _show_error(self, msg):
        """
        """
        oldy, oldx = self.scrn.getyx()
        y = self.vpad * 3  + self.n * self.vspace + 4
        x = self.hpad
        self.scrn.attron(curses.color_pair(1))
        self.scrn.addstr(y, x, "*Error!* " + msg)
        self.scrn.attroff(curses.color_pair(1))
        self.scrn.move(oldy, oldx)

