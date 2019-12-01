#!/usr/bin/env python3
"""game.py: Facilitates games between engines (or humans)."""
import sys
import chess
from engine import Brick, Gauss, Napoleon, Alpha, WeightedAlpha

def usage():
    """Prints expected command line arguments."""
    print("Usage: python3 game.py <color> <engine name>")

def play_game(type_a, type_b):
    """Runs a game between two engines.

    Args:
    type_a -- The type of the engine that will play white.
    type_b -- The type of the engine that will play black.

    Returns:
    (win string, board)
    win string is "white" if white wins, "black" if black wins, "draw" if neither won.
    board is the chess.Board object storing the game history.
    """

    engw = type_a(chess.WHITE)
    engb = type_b(chess.BLACK)
    board = chess.Board()
    while not board.is_game_over(claim_draw=True):
        if board.turn == chess.WHITE:
            move = engw.move(board)
            board.push(move)
        else:
            move = engb.move(board)
            board.push(move)
    winner = ""
    if board.is_checkmate():
        winner = "white" if board.turn == chess.BLACK else "black"
    else:
        winner = "draw"
    return (winner, board)

def headtohead(engines, num_games):
    """Runs some number of chess games for every pair of engines.

    Args:
    engines -- A list of engine types to pair off.
    num_games -- The number of games to run between each pair of engines.
    """

    # List of tuples: First elem plays white, second black
    combos = list()
    for type_a in engines:
        for type_b in engines:
            if type_a != type_b:
                combos.append((type_a, type_b))

    for combo in combos:
        wwins = 0
        bwins = 0
        draws = 0
        for game in range(0, num_games):
            res = play_game(combo[0], combo[1])
            if res[0] == "white":
                wwins += 1
            elif res[0] == "black":
                bwins += 1
            else:
                draws += 1
        print(f"{combo[0].__name__} : {combo[1].__name__} went {wwins}W/{bwins}B/{draws}D")

# TODO: Make a "player" engine and change the cmd line interface
def player():
    """Runs a game between a human player and the engine they specify in the cmd line arguments."""
    player_col = chess.WHITE
    if sys.argv[1] == 'B':
        player_col = chess.BLACK

    # If they specified an engine
    engine_type = Brick
    if len(sys.argv) > 2:
        engine_type = {
            "Brick" : Brick,
            "Gauss" : Gauss,
            "Napoleon" : Napoleon,
            "Alpha" : Alpha
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

headtohead([Brick, Gauss, Napoleon, Alpha, WeightedAlpha], 100)
