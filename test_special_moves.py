from unittest import TestCase

from bitboard import Bitboard
from bitboard_collections import ChessBitboards, SpecialMoveBitboards
from move import Move
from square import Square


class TestSpecialMoveBitboards(TestCase):

    def setUp(self) -> None:
        self.queens_side_rooks:Bitboard = Bitboard.from_square(Square(1))|Bitboard.from_square(Square(57))
        self.kings_side_rooks:Bitboard = Bitboard.from_square(Square(8))|Bitboard.from_square(Square(64))

        self.new_game:SpecialMoveBitboards = SpecialMoveBitboards(
                castling_rooks=self.queens_side_rooks|self.kings_side_rooks,
                castling_kings=Bitboard.from_square(Square(5))|Bitboard.from_square(Square(61)),
                ep_bitboard=Bitboard(0))

        self.all_castling: Bitboard = self.new_game.castling_rooks | self.new_game.castling_kings

        self.new_game_chess_bitboards:ChessBitboards = ChessBitboards.new_game()

        self.move_a2_pawn_to_a4:Move = Move(frm=Square.a2, to=Square.a4)
        self.ep_after_a2_to_a4: Bitboard = Bitboard.from_square(Square.a3)
        self.move_a7_pawn_to_a5:Move = Move(frm=Square.a7, to=Square.a5)
        self.ep_after_a7_to_a5: Bitboard = Bitboard.from_square(Square.a6)

        self.move_white_king:Move = Move(to=Square.d5, frm=Square.e1)
        self.move_black_king:Move = Move(to=Square.d5, frm=Square.e8)

        self.move_black_kingside_rook:Move = Move(frm=Square.h8, to=Square.d5)
        self.move_black_queenside_rook:Move = Move(frm=Square.a8, to=Square.d5)

        self.move_white_kingside_rook:Move = Move(frm=Square.h1, to=Square.d5)
        self.move_white_queenside_rook:Move = Move(frm=Square.a1, to=Square.d5)

    def test_new_game(self):
        self.assertEqual(self.new_game, SpecialMoveBitboards.new_game())

    def test_queenside_castling(self):
        self.assertEqual(self.queens_side_rooks, self.new_game.queenside_castling)

    def test_kingside_castling(self):
        self.assertEqual(self.kings_side_rooks, self.new_game.kingside_castling)

    def test_update_white_ep(self):
        result = self.new_game.update(self.new_game_chess_bitboards, self.move_a2_pawn_to_a4)
        self.assertEqual(self.all_castling, result.castling_rooks | result.castling_kings)
        self.assertEqual(self.ep_after_a2_to_a4, result.ep_bitboard)

    def test_update_black_ep(self):
        result = self.new_game.update(self.new_game_chess_bitboards, self.move_a7_pawn_to_a5)
        self.assertEqual(self.all_castling, result.castling_rooks | result.castling_kings)
        self.assertEqual(self.ep_after_a7_to_a5, result.ep_bitboard)

    def test_update_white_king(self):
        result = self.new_game.update(self.new_game_chess_bitboards, self.move_white_king)
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(self.queens_side_rooks|self.kings_side_rooks, result.castling_rooks)
        self.assertEqual(Bitboard.from_square(Square.e8), result.castling_kings)

    def test_update_black_king(self):
        result = self.new_game.update(self.new_game_chess_bitboards, self.move_black_king)
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(self.queens_side_rooks|self.kings_side_rooks, result.castling_rooks)
        self.assertEqual(Bitboard.from_square(Square.e1), result.castling_kings)

    def test_update_white_kingside_rook(self):
        kings = self.new_game.castling_kings
        result = self.new_game.update(self.new_game_chess_bitboards, self.move_white_kingside_rook)
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(kings, result.castling_kings)
        self.assertEqual(~Bitboard.from_square(Square.h1) & (self.queens_side_rooks|self.kings_side_rooks), result.castling_rooks)

    def test_update_white_queenside_rook(self):
        kings = self.new_game.castling_kings
        result = self.new_game.update(self.new_game_chess_bitboards, self.move_white_queenside_rook)
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(kings, result.castling_kings)
        self.assertEqual(~Bitboard.from_square(Square.a1) & (self.queens_side_rooks|self.kings_side_rooks), result.castling_rooks)

    def test_update_black_kingside_rook(self):
        kings = self.new_game.castling_kings
        result = self.new_game.update(self.new_game_chess_bitboards, self.move_black_kingside_rook)
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(kings, result.castling_kings)
        self.assertEqual(~Bitboard.from_square(Square.h8) & (self.queens_side_rooks|self.kings_side_rooks), result.castling_rooks)

    def test_update_black_queenside_rook(self):
        kings = self.new_game.castling_kings
        result = self.new_game.update(self.new_game_chess_bitboards, self.move_black_queenside_rook)
        self.assertEqual(Bitboard(0), result.ep_bitboard)
        self.assertEqual(kings, self.new_game.castling_kings)
        self.assertEqual(~Bitboard.from_square(Square.a8) & (self.queens_side_rooks|self.kings_side_rooks), result.castling_rooks)
