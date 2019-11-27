import chess
import sys
import random

    
# Abstract base class for Engines
class Engine:
    def __init__(self, color):
        self._color = color

    def move:
        raise NotImplementedError()

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
class Brick(Engine):
    def __init__(self, color):
        super().__init__(color)

    def move(self, board):
        cboard = board.copy()
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

# Picks a random legal move
class Gauss(Engine):
    def __init__(self, color):
        super().__init__(color)

    def move(self, board):
        return random.choice(list(board.legal_moves))


# Picks a move that immediately reduces your material. Breaks ties randomly
class Napoleon(Engine):
    self._table = {
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
        cboard = board.copy()
        moves = list(cboard.legal_moves)
        minmaterial = 2000
        minmove = moves[0]
        for move in moves:
            cboard.push(move)
            value = self.board_eval(cboard)
            if value < minmaterial:
                minmaterial = value
                minmove = move
            cboard.pop()
        return minmove

# Tries to maximize the number of attacks they have on your pieces minus the number of attacks you have on theirs
class Alpha(Engine):
    self._table = {
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
        cboard = board.copy()
        moves = list(cboard.legal_moves)
        minmaterial = 2000
        minmove = moves[0]
        for move in moves:
            cboard.push(move)
            value = self.board_eval(cboard)
            if value < minmaterial:
                minmaterial = value
                minmove = move
            cboard.pop()
        return minmove

# Ideas:
# Gogh: Protects black square bishop at all costs.
# Unnamed: Tries to maximize number of attacks they have on your pieces minus number of attacks you have on theirs. (Could be weighted by piece value)
# Multi: Runs the move through multiple other engines and decides randomly among the ones that didnt "fall back" to random (if they all fell back to random, do a random move)

