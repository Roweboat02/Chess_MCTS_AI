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
        a1:Square = Square.a1
        a1_goal:Bitboard = (Bitboard.from_square(Square.b2)|
                            Bitboard.from_square(Square.c3)|
                            Bitboard.from_square(Square.d4)|
                            Bitboard.from_square(Square.e5)|
                            Bitboard.from_square(Square.f6)|
                            Bitboard.from_square(Square.g7)|
                            Bitboard.from_square(Square.h8))

        f3:Square = Square.f3
        f3_occupied = Bitboard.from_square(Square.e2)
        f3_goal:Bitboard = (Bitboard.from_square(Square.b7) |
                            Bitboard.from_square(Square.c6) |
                            Bitboard.from_square(Square.d5) |
                            Bitboard.from_square(Square.e4) |
                            Bitboard.from_square(Square.a8) |
                            Bitboard.from_square(Square.g2) |
                            Bitboard.from_square(Square.h1) |
                            Bitboard.from_square(Square.g4) |
                            Bitboard.from_square(Square.h5)) | f3_occupied


        a1_result = diagonal_moves(a1, Bitboard(0))

        # a_r = format(a1_result, '064b')
        # a_g = format(a1_goal, "064b")
        # print("a1_result")
        # for i in range(0, 65, 8):
        #     print(a_r[i : i+8])
        # print("a1_goal")
        # for i in range(0, 65, 8):
        #     print(a_g[i : i+8])

        self.assertEqual(a1_goal, a1_result)
        # print("\n\n\n\n")

        f3_result = diagonal_moves(f3, f3_occupied)
        # print("f3_result")
        # f_r = format(f3_result, '064b')
        # f_g = format(f3_goal, '064b')
        # for i in range(0, 65, 8):
        #     print(f_r[i : i+8])
        # print("f3_goal")
        # for i in range(0, 65, 8):
        #     print(f_g[i : i+8])
        self.assertEqual(f3_goal, f3_result)


    def test_piece_move_mask(self):
        on_c2 = Square.c2
        rook = (Bitboard.from_file(3)|Bitboard.from_rank(2))&~Bitboard.from_square(on_c2)
        bishop = reduce_with_bitwise_or(Bitboard.from_square(s) for s in [Square.b1, Square.d1, Square.b3, Square.a4, Square.d3, Square.e4, Square.f5, Square.g6, Square.h7])
        knight = reduce_with_bitwise_or(Bitboard.from_square(s) for s in [Square.b4, Square.d4, Square.a3, Square.e3, Square.e1, Square.a1])
        queen = rook|bishop
        king = reduce_with_bitwise_or(Bitboard.from_square(s) for s in [Square.c3, Square.c1, Square.b3, Square.b2, Square.b1, Square.d3, Square.d2, Square.d1,])

        self.assertEqual(rook, piece_move_mask(on_c2, Piece.r, Bitboard(0)))
        self.assertEqual(rook, piece_move_mask(on_c2, Piece.R, Bitboard(0)))

        self.assertEqual(bishop, piece_move_mask(on_c2, Piece.b, Bitboard(0)))
        self.assertEqual(bishop, piece_move_mask(on_c2, Piece.B, Bitboard(0)))

        self.assertEqual(knight, piece_move_mask(on_c2, Piece.n, Bitboard(0)))
        self.assertEqual(knight, piece_move_mask(on_c2, Piece.N, Bitboard(0)))

        self.assertEqual(queen, piece_move_mask(on_c2, Piece.q, Bitboard(0)))
        self.assertEqual(queen, piece_move_mask(on_c2, Piece.Q, Bitboard(0)))

        self.assertEqual(king, piece_move_mask(on_c2, Piece.k, Bitboard(0)))
        self.assertEqual(king, piece_move_mask(on_c2, Piece.K, Bitboard(0)))
