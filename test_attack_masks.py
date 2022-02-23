from unittest import TestCase
from attack_masks import *

class TestAttackMasks(TestCase):
    def test_pawn_attacks(self):
        a2:Square = Square.a2
        white_a2:Bitboard = Bitboard.from_square(Square.b3)
        black_a2:Bitboard = Bitboard.from_square(Square.b1)

        d5:Square = Square.d5
        white_d5:Bitboard = Bitboard.from_square(Square.e6) | Bitboard.from_square(Square.c6)
        black_d5:Bitboard = Bitboard.from_square(Square.c4) | Bitboard.from_square(Square.e4)

        h8:Square = Square.h8
        white_h8:Bitboard = Bitboard(0)
        black_h8:Bitboard = Bitboard.from_square(Square.g7)

        self.assertEqual( white_a2, pawn_attacks(a2, True))
        self.assertEqual( black_a2, pawn_attacks(a2, False))

        self.assertEqual( white_d5, pawn_attacks(d5, True))
        self.assertEqual( black_d5, pawn_attacks(d5, False))

        self.assertEqual( white_h8, pawn_attacks(h8, True))
        self.assertEqual( black_h8, pawn_attacks(h8, False))

    def test_knight_moves(self):
        h8 = Square.h8
        h8_moves = Bitboard.from_square(Square.f7) | Bitboard.from_square(Square.g6)

        e4 = Square.e4
        e4_moves = Bitboard.from_square(Square.d6)|Bitboard.from_square(Square.f6)|Bitboard.from_square(Square.g5)|Bitboard.from_square(Square.g3)|Bitboard.from_square(Square.f2)|Bitboard.from_square(Square.d2)|Bitboard.from_square(Square.c3)|Bitboard.from_square(Square.c5)

        self.assertEqual(h8_moves, knight_moves(h8))
        self.assertEqual(e4_moves, knight_moves(e4))


    def test_king_moves(self):
        h8 = Square.h8
        h8_moves = Bitboard.from_square(Square.g8) | Bitboard.from_square(Square.g7) | Bitboard.from_square(Square.h7)

        e4 = Square.e4
        e4_moves = Bitboard.from_square(Square.d5)|Bitboard.from_square(Square.d4)|Bitboard.from_square(Square.d3)|Bitboard.from_square(Square.e3)|Bitboard.from_square(Square.e5)|Bitboard.from_square(Square.f5)|Bitboard.from_square(Square.f4)|Bitboard.from_square(Square.f3)

        self.assertEqual(h8_moves, king_moves(h8))
        self.assertEqual(e4_moves, king_moves(e4))

    def test_rank_moves(self):
        d5:Square = Square.d5
        d5_moves:Bitboard = Bitboard.from_rank(5) & ~Bitboard.from_square(d5)
        d5_occupied:Bitboard = Bitboard(0)

        self.assertEqual(d5_moves, rank_moves(d5, d5_occupied))

        a1:Square = Square.a1
        a1_occupied:Bitboard = Bitboard.from_square(Square.f1)
        a1_moves:Bitboard = Bitboard.from_rank(1) & ~(Bitboard.from_square(Square.g1) | Bitboard.from_square(Square.h1) | Bitboard.from_square(a1))
        self.assertEqual(a1_moves, rank_moves(a1, a1_occupied))


    def test_file_moves(self):
        d5: Square = Square.d5
        d5_moves: Bitboard = Bitboard.from_file(4) & ~Bitboard.from_square(d5)
        d5_occupied: Bitboard = Bitboard(0)

        self.assertEqual(d5_moves, file_moves(d5, d5_occupied))

        a1: Square = Square.a1
        a1_occupied: Bitboard = Bitboard.from_square(Square.a7)
        a1_moves: Bitboard = Bitboard.from_file(1) & ~(Bitboard.from_square(Square.a8) | Bitboard.from_square(a1))
        self.assertEqual(a1_moves, file_moves(a1, a1_occupied))

    def test_diagonal_moves(self):
        self.fail()

    def test_piece_move_mask(self):
        self.fail()
