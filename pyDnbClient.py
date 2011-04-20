#!/usr/bin/python

from sys import argv, exit, exc_info
from os import system
from socket import socket, AF_INET, SOCK_STREAM
from curses import initscr, cbreak, noecho, echo, start_color, init_pair, color_pair, COLOR_WHITE, COLOR_RED, A_UNDERLINE, A_BOLD
from cPickle import dumps, loads
from traceback import print_tb
from GameUi import GameUi
from Msgs import *


vspace = 3
hspace = 3
title = 'pyDnb - Dots and Boxes Game'
y = 0
host = ''
port = 0

def main(args):
    global host
    global port
    host = args[1]
    port = int(args[2])
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    init(s)
    s.close()

def init(sock):
    scrn = initscr()
    cbreak()
    start_color()
    init_pair(1, COLOR_WHITE, COLOR_RED)

    try:
        while True:
            msg = sock.recv(SIZE)

            if msg == SERVER_FULL:
                txt1 = 'Maximum player limit is reached'
                txt2 = 'Press e to exit'
                x, y = (scrn.getmaxyx()[1] - len(txt1)) / 2, 2
                scrn.addstr(y, x, txt1)
                #x, y = (scrn.getmaxyx()[1] - len(txt2)) / 2, 3
                #scrn.addstr(y, x, txt2)
                noecho()

                ch = scrn.getkey()
                while True:
                    if ch == 'q':
                        system('clear')
                        exit(0)
                    else:
                        ch = scrn.getkey()

            n = game_selection(scrn, sock)

            if n != -1:
                game = GameUi(sock, scrn, n)
                game.init_game()
                break
            else:
                while True:
                    sock.send(dumps([DELPLAYER]))
                    msg = sock.recv(SIZE)
                    if msg == SDELP:
                        sock.close()
                        sock = socket(AF_INET, SOCK_STREAM)
                        sock.connect((host, port))
                        break
    except KeyboardInterrupt:
        sock.send(dumps([DELPLAYER]))
        msg = sock.recv(SIZE)
        sock.close()
        exc_type, exc_value, exc_traceback = exc_info()
        print_tb(exc_traceback)

def game_selection(scrn, sock):
    global y
    scrn.addstr(y+1, hspace, '%50s' % ' ')
    sock.send(dumps([GAME_LIST]))
    raw_list = sock.recv(SIZE)
    game_list = loads(raw_list)

    x, y = (scrn.getmaxyx()[1] - len(title)) / 2, 0
    scrn.addstr(y, x, title)
    if game_list:
        scrn.attron(A_UNDERLINE | A_BOLD)
        scrn.addstr(2, hspace, "%-6s%-13s%-13s%-10s" % ('#', 'Game', 'Board Size', 'Capacity'))
        scrn.attroff(A_UNDERLINE | A_BOLD)

        y = vspace
        i = 0
        while i < len(game_list):
            scrn.addstr(y + i, hspace, '%(i)-6dGame %(i)-8d%(n)-13d%(cap)-10s' % game_list[i])
            i += 1
        y += i
    else:
        x, y = hspace, vspace
        scrn.addstr(y, x, NO_GAME)

    scrn.addstr(y+1, hspace, 'Enter choice (c: create game, j: join game, e: exit): ')
    #noecho()
    ch = scrn.getkey()
    while True:
        if ch == 'c':
            scrn.addstr(y+2, hspace, 'Press u for upper menu')
            scrn.addstr(y+1, hspace, 'Enter dot number: %40s' % ' ')
            number = get_number(scrn, 10)
            if number == -1:
                scrn.addstr(y+1, hspace, 'Enter choice (c: create game, j: join game, e: exit): ')
                scrn.addstr(y+2, hspace, '%40s' % ' ')
                scrn.move(y+1, hspace + 54)
                ch = scrn.getkey()
                continue
            return create_game(scrn, sock, number)
            break
        elif ch == 'j':
            scrn.addstr(y+2, hspace, 'Press u for upper menu')
            scrn.addstr(y+1, hspace, 'Enter game number: %40s' % ' ')
            number = get_number(scrn, len(game_list) - 1)
            if number == -1:
                scrn.addstr(y+1, hspace, 'Enter choice (c: create game, j: join game, e: exit): ')
                scrn.addstr(y+2, hspace, '%40s' % ' ')
                scrn.move(y+1, hspace + 54)
                ch = scrn.getkey()
                continue
            return join_game(scrn, sock, number, game_list)
            break
        elif ch == 'e':
            system('clear')
            exit(0)
        else:
            scrn.addstr(y+2, hspace, '%40s' % ' ')
            scrn.attron(color_pair(1))
            scrn.addstr(y+2, hspace, 'Wrong selection!')
            scrn.attroff(color_pair(1))
            scrn.move(y+1, hspace + 54)
            ch = scrn.getkey()

def create_game(scrn, sock, n):
    """
    """
    msg = [CREATE, n]
    sock.send(dumps(msg))
    resp = sock.recv(SIZE)
    if resp == SCREATE:
        return n
    else:
        scrn.addstr(y+2, hspace, '%40s' % ' ')
        scrn.attron(color_pair(1))
        scrn.addstr(y+2, hspace, 'Game cannot be created. Maximum game limit reached!')
        scrn.attroff(color_pair(1))
        scrn.move(y+1, hspace + 54)
        return -1


def join_game(scrn, sock, i, games):
    '''
    '''
    msg = [JOIN, i]
    sock.send(dumps(msg))
    resp = sock.recv(SIZE)
    if resp == SJOIN:
        return games[i]['n']
    else:
        scrn.addstr(y+2, hspace, '%40s' % ' ')
        scrn.attron(color_pair(1))
        scrn.addstr(y+2, hspace, 'Cannot join to the game. Game is full!')
        scrn.attroff(color_pair(1))
        scrn.move(y+1, hspace + 54)
        return -1

def get_number(scrn, default):
    """
    """
    global y
    echo()
    while True:
        number = []
        scrn.addstr(y+1, hspace + 20, '%25s' % ' ')
        scrn.move(y+1, hspace + 20)
        ch = scrn.getkey()
        scrn.addstr(y+3, hspace, '%35s' % ' ')
        scrn.move(y+1, hspace + 21)
        while ch != '\n':
            number.append(ch)
            ch = scrn.getkey()

        number = ''.join(number)
        try:
            if number == 'u':
                return -1
            number = int(number)
            if number > default or number < 0:
                raise Exception()
            break
        except:
            scrn.attron(color_pair(1))
            scrn.addstr(y+3, hspace, 'Not a number or too big (max %d) ' % default)
            scrn.attroff(color_pair(1))

    return number

if __name__ == "__main__":
    main(argv)
