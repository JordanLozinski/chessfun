#!/usr/bin/python3 

import chess
import sys
import random
from engine import Brick, Gauss, Napoleon

# python game.py <color> <engine_name>
def usage():
    pass

def main():
    player_col = chess.WHITE
    if sys.argv[1] == 'B':
        player_col = chess.BLACK
    
    # If they specified an engine
    engine_type = Brick
    if len(sys.argv) > 2:
        engine_type = {
            "Brick" : Brick,
            "Gauss" : Gauss,
            "Napoleon" : Napoleon
        }[sys.argv[2]]


    engine = engine_type(not player_col)
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == player_col:
            print(board if player_col == chess.WHITE else board.mirror())
            inmove = input("SAN move: ")
            try:
                move = board.parse_san(inmove)
            except ValueError:
                print("Invalid move, try again")
            else:
                board.push(move)
        else:
            move = engine.move(board)
            try:
                board.push(move)
            except ValueError:
                print("Engine attempted invalid move " + move.uci())

main()
