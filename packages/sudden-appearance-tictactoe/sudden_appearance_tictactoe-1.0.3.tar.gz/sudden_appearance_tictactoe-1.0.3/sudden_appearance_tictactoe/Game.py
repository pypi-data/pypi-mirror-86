import argparse
import random

from Grid import Grid
from O import O
from X import X


def run():
    parser = argparse.ArgumentParser(description="Tic-tac-toe game. 2 players. To make a move command <"
                                                 "[x] [y]>, x - pos left, y - pos right")
    a = Grid()
    finished = None
    players = [X(), O()]
    player = random.randint(0, 1)
    while not finished:
        try:
            print(a)
            move = input(f"{players[player]}'s move\n").split()
            a.insert(int(move[0]), int(move[1]), players[player])
            player = 1 - player
            finished = a.over()
        except IndexError or ValueError:
            print("Incorrect move. Try again")
            continue
        except IOError:
            print("This spot is already taken. Try again")
            continue
    print(a)
    if finished == "Draw":
        print("Draw")
    else:
        print(str(finished) + " won")
