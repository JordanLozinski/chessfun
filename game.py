#!/usr/bin/python3 

import chess
import sys
import random

class Engine:
    def __init__(self, color):
        self._color = color

    def move(self, board):
        cboard = chess.Board(fen=board.fen(promoted=board.promoted))
        moves = list(cboard.legal_moves)
        random.shuffle(moves)
        minlen = sys.maxsize
        minmove = moves[0]
        for move in moves:
            cboard.push(move)
            if cboard.legal_moves.count() < minlen:
                minlen = cboard.legal_moves.count()
                minmove = move
            cboard.pop()
        return minmove

# python game.py <color>
def usage():
    pass

def main():
    player_col = chess.WHITE
    if sys.argv[1] == 'B':
        player_col = chess.BLACK
    
    engine = Engine(not player_col)
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == player_col:
            print(board)
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
