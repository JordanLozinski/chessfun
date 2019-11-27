import chess
import sys
import random

    
# Abstract base class for Engines
class Engine:
    def __init__(self, color):
        self._color = color

    def move(self, board):
        raise NotImplementedError()

# Picks a random legal move
class Gauss(Engine):
    def __init__(self, color):
        super().__init__(color)

    def move(self, board):
        return random.choice(list(board.legal_moves))

# Picks the move that immediately minimizes whatever evaluation function you give it. Ties broken randomly
class Minimizer(Engine):
    def __init__(self, color):
        super().__init__(color)

    def move(self, board, board_eval):
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

# Tries to minimize the number of moves you can do next round. Breaks ties randomly
class Brick(Minimizer):
    def __init__(self, color):
        super().__init__(color)

    def board_eval(self, board):
        return cboard.legal_moves

    def move(self, board):
        return super().move(board, self.board_eval)

# Picks a move that immediately reduces your material. Breaks ties randomly
class Napoleon(Minimizer):
    _table = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.25,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1000
    }
    
    def __init__(self, color):
        super().__init__(color)

    # Count up the material value of the opponent
    def board_eval(self, board):
        tot = 0
        # For each piece type
        for ty in self._table:
            # tot += piece value * how many of that piece the opponent has
            tot += self._table[ty]*len(board.pieces(ty, not self._color))
        return tot

    def move(self, board):
        return super().move(board, self.board_eval)

# Tries to maximize the number of attacks they have on your pieces minus the number of attacks you have on theirs
class Alpha(Engine):
    pass

# Ideas:
# Gogh: Protects black square bishop at all costs.
# Unnamed: Tries to maximize number of attacks they have on your pieces minus number of attacks you have on theirs. (Could be weighted by piece value)
# Multi: Runs the move through multiple other engines and decides randomly among the ones that didnt "fall back" to random (if they all fell back to random, do a random move)

