#!/usr/bin/python

from sys import argv
from os import system

from GameServer import GameServer

def main(args):
    server = GameServer(1, argv[1], int(argv[2]))
    server.start_server()



if __name__ == '__main__':
    main(argv)
