"""engine.py: Implements a variety of simple chess engines."""
import sys
import random
from abc import ABC, abstractmethod
import chess

class Engine(ABC):
    """Abstract base class for chess engines."""
    def __init__(self, color):
        self._color = color

    @abstractmethod
    def move(self, board):
        return

    @staticmethod
    def min_move(board, board_eval):
        """Picks the legal move that minimizes the supplied board evaluation function."""
        cboard = board.copy()
        moves = list(cboard.legal_moves)
        random.shuffle(moves)
        minval = sys.maxsize
        minmove = moves[0]
        for move in moves:
            cboard.push(move)
            val = board_eval(cboard)
            if val < minval:
                minval = val
                minmove = move
            cboard.pop()
        return minmove

class Gauss(Engine):
    """Picks a random legal move."""

    def move(self, board):
        return random.choice(list(board.legal_moves))

class Brick(Engine):
    """Minimizes the number of moves its opponent can do their next turn."""

    def board_eval(self, board):
        return board.legal_moves.count()

    def move(self, board):
        return super().min_move(board, self.board_eval)

class Napoleon(Engine):
    """Picks the move that most reduces its opponent's material."""
    _table = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3.25,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 1000
    }

    def board_eval(self, board):
        """Counts up the material value of the opponent."""
        tot = 0
        # For each piece type
        for piecetype in self._table:
            # tot += piece value * how many of that piece the opponent has
            tot += self._table[piecetype]*len(board.pieces(piecetype, not self._color))
        return tot

    def move(self, board):
        return super().min_move(board, self.board_eval)

class Alpha(Engine):
    """Minimizes the number of attacks on it minus
    the number of attacks it has."""

    def board_eval(self, board):
        num_attacking = 0
        num_attacks = 0
        for piecetype in [chess.PAWN, chess.KNIGHT, chess.BISHOP,
                          chess.ROOK, chess.QUEEN, chess.KING]:
            # Iterate through opponent's pieces of piecetype
            for piece in board.pieces(piecetype, not self._color):
                # Count the number of your attackers each of the opponent's
                # pieces have.
                num_attacking += len(list(board.attackers(self._color, piece)))
            
            # Iterate through your own pieces of piecetype
            for piece in board.pieces(piecetype, self._color):
                # Count the number of your opponent's attackers each of your
                # pieces have.
                num_attacks += len(list(board.attackers(not self._color, piece)))
        return num_attacks - num_attacking

    def move(self, board):
        return super().min_move(board, self.board_eval)

class WeightedAlpha(Engine):
    """Minimizes the number of attacks on it minus
    the number of attacks it has."""
    _table = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3.25,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 1000
    }

    def board_eval(self, board):

        num_attacking = 0
        num_attacks = 0
        for piecetype in [chess.PAWN, chess.KNIGHT, chess.BISHOP,
                          chess.ROOK, chess.QUEEN, chess.KING]:
            # Iterate through opponent's pieces of piecetype
            for piece in board.pieces(piecetype, not self._color):
                # Count the number of your attackers each of the opponent's
                # pieces have.
                num_attacking += self._table[piecetype] * len(list(board.attackers(self._color, piece)))
            
            # Iterate through your own pieces of piecetype
            for piece in board.pieces(piecetype, self._color):
                # Count the number of your opponent's attackers each of your
                # pieces have.
                num_attacks += self._table[piecetype] * len(list(board.attackers(not self._color, piece)))
        return num_attacks - num_attacking

    def move(self, board):
        return super().min_move(board, self.board_eval)

# Ideas:
# Gogh: Protects black square bishop at all costs.
# Multi: Runs the move through multiple other engines and decides
# among the ones that didnt "fall back" to random
