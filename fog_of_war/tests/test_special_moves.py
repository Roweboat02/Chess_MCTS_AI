"""
test_special_moves.py
Tests for chess special move bitboard collection functionality.

Author: Noah Rowe
Date: 2022/02/22
Last Modified: 2022/02/23
    Added docstrings
"""
from unittest import TestCase

from fog_of_war.bitboard import Bitboard
from fog_of_war.chess_bitboards import ChessBitboards
from fog_of_war.special_move_bitboards import SpecialMoveBitboards
from fog_of_war.move import Move
from fog_of_war.square import Square


class TestSpecialMoveBitboards(TestCase):
    """Special move tests"""

    def setUp(self) -> None:
        """Set up"""
        self.queens_side_rooks: Bitboard = (Bitboard.from_square(Square.a1)
                                            | Bitboard.from_square(Square.a8))
        self.kings_side_rooks: Bitboard = (Bitboard.from_square(Square.h1)
                                           | Bitboard.from_square(Square.h8))

        self.new_game: SpecialMoveBitboards = SpecialMoveBitboards(
            castling_rooks=self.queens_side_rooks | self.kings_side_rooks,
            castling_kings=Bitboard.from_square(Square.e1) | Bitboard.from_square(Square.e8),
            ep_bitboard=Bitboard(0))

        self.all_castling: Bitboard = self.new_game.castling_rooks | self.new_game.castling_kings

        self.new_game_chess_bitboards: ChessBitboards = ChessBitboards.new_game()

    def test_new_game(self):
        """Test if new_game alt constructor is working"""
        self.assertEqual(self.new_game, SpecialMoveBitboards.new_game())

    def test_queen_side_castling(self):
        """Test if queen side property is working"""
        self.assertEqual(self.queens_side_rooks, self.new_game.queen_side_castling)

    def test_king_side_castling(self):
        """Test if king side property is working"""
        self.assertEqual(self.kings_side_rooks, self.new_game.king_side_castling)

    def test_update_white_ep(self):
        """
        Test if when white makes a double pawn step,
        if ep_bitboard updates correctly
        """
        move_a2_pawn_to_a4: Move = Move(frm=Square.a2, to=Square.a4)
        ep_after_a2_to_a4: Bitboard = Bitboard.from_square(Square.a3)

        result = self.new_game.update(self.new_game_chess_bitboards, move_a2_pawn_to_a4)
        self.assertEqual(self.all_castling, result.castling_rooks | result.castling_kings)
        self.assertEqual(ep_after_a2_to_a4, result.ep_bitboard)

    def test_update_black_ep(self):
        """
        Test if when black makes a double pawn step,
        if ep_bitboard updates correctly
        """
        move_a7_pawn_to_a5: Move = Move(frm=Square.a7, to=Square.a5)
        ep_after_a7_to_a5: Bitboard = Bitboard.from_square(Square.a6)

        result = self.new_game.update(self.new_game_chess_bitboards, move_a7_pawn_to_a5)
        self.assertEqual(self.all_castling, result.castling_rooks | result.castling_kings)
        self.assertEqual(ep_after_a7_to_a5, result.ep_bitboard)

    def test_update_white_king(self):
        """
        Test if when white moves their king,
        if they castling_kings updates correctly
        """
        result = self.new_game.update(self.new_game_chess_bitboards,
                                      Move(to=Square.d5, frm=Square.e1))
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(self.queens_side_rooks | self.kings_side_rooks,
                         result.castling_rooks)
        self.assertEqual(Bitboard.from_square(Square.e8), result.castling_kings)

    def test_update_black_king(self):
        """
        Test if when black moves their king,
        if they castling_kings updates correctly
        """
        result = self.new_game.update(self.new_game_chess_bitboards,
                                      Move(to=Square.d5, frm=Square.e8))
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(self.queens_side_rooks | self.kings_side_rooks,
                         result.castling_rooks)
        self.assertEqual(Bitboard.from_square(Square.e1), result.castling_kings)

    def test_update_white_king_side_rook(self):
        """
        Test if when white moves their king side rook,
        if they castling_rooks updates correctly
        """
        kings = self.new_game.castling_kings
        result = self.new_game.update(self.new_game_chess_bitboards,
                                     Move(frm=Square.h1, to=Square.d5))
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(kings, result.castling_kings)
        self.assertEqual(~Bitboard.from_square(Square.h1)
                         & (self.queens_side_rooks | self.kings_side_rooks),
                         result.castling_rooks)

    def test_update_white_queen_side_rook(self):
        """
         Test if when white moves their queen side rook,
         if they castling_rooks updates correctly
         """
        kings = self.new_game.castling_kings
        result = self.new_game.update(self.new_game_chess_bitboards,
                                      Move(frm=Square.a1, to=Square.d5))
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(kings, result.castling_kings)
        self.assertEqual(~Bitboard.from_square(Square.a1)
                         & (self.queens_side_rooks | self.kings_side_rooks),
                         result.castling_rooks)

    def test_update_black_king_side_rook(self):
        """
         Test if when black moves their king side rook,
         if they castling_rooks updates correctly
         """
        kings = self.new_game.castling_kings
        result = self.new_game.update(self.new_game_chess_bitboards,
                                      Move(frm=Square.h8, to=Square.d5))
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(kings, result.castling_kings)
        self.assertEqual(~Bitboard.from_square(Square.h8)
                         & (self.queens_side_rooks | self.kings_side_rooks),
                         result.castling_rooks)

    def test_update_black_queen_side_rook(self):
        """
         Test if when black moves their queen side rook,
         if they castling_rooks updates correctly
         """
        kings = self.new_game.castling_kings
        result = self.new_game.update(self.new_game_chess_bitboards,
                                      Move(frm=Square.a8, to=Square.d5))
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(kings, self.new_game.castling_kings)
        self.assertEqual(~Bitboard.from_square(Square.a8)
                         & (self.queens_side_rooks | self.kings_side_rooks),
                         result.castling_rooks)
