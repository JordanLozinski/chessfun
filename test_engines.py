import unittest
import chess
from engine import Alpha, WeightedAlpha


class TestAlphaEval(unittest.TestCase):
    def test_eval(self):
        a = Alpha(chess.WHITE)
        board = chess.Board()
        """
        - R B R - - K -
        P - P - - P P P
        - P K - - Q - -
        - - K - P - - -
        - - - - p B p p
        - - p - - p k -
        p p q k b b - -
        - - k r - - - r
        """
        board.set_fen("1rbr2k1/p1p2ppp/1pn2q2/2n1p3/4PbPP/2P2PN1/PPQNBB2/2KR3R w - - 1 16")
        # num_attacking should be 1 (Bc5)
        # num_attacks should be 4 (Bg3, Bd2, Qh4, Rd2, Ke4, Bg4)
        # 6 - 1 == 5
        self.assertEqual(a.board_eval(board.copy()), 5)

    def test_weighted_eval(self):
        a = WeightedAlpha(chess.WHITE)
        """
        - R B R - - K -
        P - P - - P P P
        - P K - - Q - -
        - - K - P - - -
        - - - - p B p p
        - - p - - p k -
        p p q k b b - -
        - - k r - - - r
        """
        board.set_fen("1rbr2k1/p1p2ppp/1pn2q2/2n1p3/4PbPP/2P2PN1/PPQNBB2/2KR3R w - - 1 16")
        # num_attacking should be 3 (Bc5 on knight)
        # num_attacks should be 12 (Bg3 on knight, Bd2 on knight, Qh4 on pawn, Rd2 on knight, Ke4 on pawn, Bg4 on pawn)
        self.assertEqual(a.board_eval(board.copy()), 9)
