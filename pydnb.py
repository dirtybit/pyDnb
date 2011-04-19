#!/usr/bin/python

import sys
import DnB

def main(args):
    n = args[1]
    game = DnB.DnB(n)
    game.init_game()

if __name__ == "__main__":
    main(sys.argv)
