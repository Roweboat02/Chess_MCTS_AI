"""
test_chess_bitboards.py
Tests for chess bitboard collection functionality.

Author: Noah Rowe
Date: 2022/02/22
Last Modified: 2022/02/23
    Added docstrings
"""

from typing import List
from unittest import TestCase

from fog_of_war import reduce_with_bitwise_or
from fog_of_war.bitboard import Bitboard
from fog_of_war.chess_bitboards import ChessBitboards
from fog_of_war.move import Move
from fog_of_war.piece import Piece
from fog_of_war.square import Square


class TestChessBitboards(TestCase):
    """ChessBitboard tests"""

    def setUp(self) -> None:
        """Set up"""
        self.empty: ChessBitboards = ChessBitboards(
            Bitboard(0),
            Bitboard(0),
            Bitboard(0),
            Bitboard(0),
            Bitboard(0),
            Bitboard(0),
            Bitboard(0),
            Bitboard(0))

        self.new_game: ChessBitboards = ChessBitboards(
            white=Bitboard.from_rank(1) | Bitboard.from_rank(2),

            black=Bitboard.from_rank(7) | Bitboard.from_rank(8),

            pawns=Bitboard.from_rank(2) | Bitboard.from_rank(7),

            knights=reduce_with_bitwise_or(Bitboard.from_square(Square.b1),
                                           Bitboard.from_square(Square.g1),
                                           Bitboard.from_square(Square.b8),
                                           Bitboard.from_square(Square.g8)),

            bishops=reduce_with_bitwise_or(Bitboard.from_square(Square.c1),
                                           Bitboard.from_square(Square.f1),
                                           Bitboard.from_square(Square.c8),
                                           Bitboard.from_square(Square.f8)),

            rooks=reduce_with_bitwise_or(Bitboard.from_square(Square.a1),
                                         Bitboard.from_square(Square.h1),
                                         Bitboard.from_square(Square.a8),
                                         Bitboard.from_square(Square.h8)),

            queens=Bitboard.from_square(Square.d1) | Bitboard.from_square(Square.d8),
            kings=Bitboard.from_square(Square.e1) | Bitboard.from_square(Square.e8))

    def test_new_game(self):
        """Test i alt constructor for a new game is correct"""
        self.assertEqual(ChessBitboards.new_game(), self.new_game)

    def test_piece_at(self):
        """Test if piece at returns the proper piece from square"""
        white: List[Piece] = [Piece.R,
                              Piece.N,
                              Piece.B,
                              Piece.Q,
                              Piece.K,
                              Piece.B,
                              Piece.N,
                              Piece.R]

        black: List[Piece] = [Piece.r,
                              Piece.n,
                              Piece.b,
                              Piece.q,
                              Piece.k,
                              Piece.b,
                              Piece.n,
                              Piece.r]

        for i in Square:
            self.assertIsNone(self.empty.piece_at(i))

        for i in range(1, 9):
            self.assertEqual(self.new_game.piece_at(Square(i)), white[i - 1])

        for i in range(57, 65):
            self.assertEqual(self.new_game.piece_at(Square(i)), black[(i - 1) % 8])

        for i in range(9, 17):
            self.assertEqual(self.new_game.piece_at(Square(i)), Piece.P)

        for i in range(49, 57):
            self.assertEqual(self.new_game.piece_at(Square(i)), Piece.p)

        for i in range(17, 49):
            self.assertIsNone(self.new_game.piece_at(Square(i)))

    def test_make_move(self):
        """Test if bitboards make regular moves correctly"""
        result = self.new_game.make_move(Move(frm=Square.a2, to=Square.a4))
        move_a2_pawn_forward: ChessBitboards = ChessBitboards(
            white=(Bitboard.from_rank(1)
                   | (Bitboard.from_rank(2)
                      & ~Bitboard.from_square(Square.a2))
                   | Bitboard.from_square(Square.a4)),

            black=Bitboard.from_rank(7) | Bitboard.from_rank(8),

            pawns=((Bitboard.from_rank(2)
                    & ~Bitboard.from_square(Square.a2))
                   | Bitboard.from_square(Square.a4)
                   | Bitboard.from_rank(7)),

            knights=reduce_with_bitwise_or(
                Bitboard.from_square(Square.b1),
                Bitboard.from_square(Square.g1),
                Bitboard.from_square(Square.b8),
                Bitboard.from_square(Square.g8)),

            bishops=reduce_with_bitwise_or(
                Bitboard.from_square(Square.c1),
                Bitboard.from_square(Square.f1),
                Bitboard.from_square(Square.c8),
                Bitboard.from_square(Square.f8)),

            rooks=reduce_with_bitwise_or(
                Bitboard.from_square(Square.a1),
                Bitboard.from_square(Square.h1),
                Bitboard.from_square(Square.a8),
                Bitboard.from_square(Square.h8)),
            queens=Bitboard.from_square(Square.d1) | Bitboard.from_square(Square.d8),
            kings=Bitboard.from_square(Square.e1) | Bitboard.from_square(Square.e8))

        self.assertFalse(self.new_game == result)
        self.assertIsNone(result.piece_at(Square.a2))
        self.assertEqual(Piece.P, result.piece_at(Square.a4))
        self.assertEqual(move_a2_pawn_forward, result)
    # TODO: Test promotions and castling
