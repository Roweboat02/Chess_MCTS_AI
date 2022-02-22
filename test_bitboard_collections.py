from typing import List
from unittest import TestCase
from bitboard import Bitboard
from bitboard_collections import ChessBitboards, SpecialMoveBitboards
from move import Move
from piece import Piece
from square import Square


class TestChessBitboards(TestCase):
    def setUp(self) -> None:
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
                knights=Bitboard.from_square(Square(2)) | Bitboard.from_square(Square(7)) | Bitboard.from_square(
                    Square(58)) | Bitboard.from_square(Square(63)),
                bishops=Bitboard.from_square(Square(3)) | Bitboard.from_square(Square(6)) | Bitboard.from_square(
                    Square(59)) | Bitboard.from_square(Square(62)),
                rooks=Bitboard.from_square(Square(1)) | Bitboard.from_square(Square(8)) | Bitboard.from_square(
                    Square(57)) | Bitboard.from_square(Square(64)),
                queens=Bitboard.from_square(Square(4)) | Bitboard.from_square(Square(60)),
                kings=Bitboard.from_square(Square(5)) | Bitboard.from_square(Square(61)))

        self.move_a2_pawn_forward: ChessBitboards = ChessBitboards(
                white=Bitboard.from_rank(1) | (
                            Bitboard.from_rank(2) & ~Bitboard.from_square(Square(9))) | Bitboard.from_square(
                    Square(17)),
                black=Bitboard.from_rank(7) | Bitboard.from_rank(8),
                pawns=(Bitboard.from_rank(2) & ~Bitboard.from_square(Square(9))) | Bitboard.from_square(
                    Square(17)) | Bitboard.from_rank(7),
                knights=Bitboard.from_square(Square(2)) | Bitboard.from_square(Square(7)) | Bitboard.from_square(
                    Square(58)) | Bitboard.from_square(Square(63)),
                bishops=Bitboard.from_square(Square(3)) | Bitboard.from_square(Square(6)) | Bitboard.from_square(
                    Square(59)) | Bitboard.from_square(Square(62)),
                rooks=Bitboard.from_square(Square(1)) | Bitboard.from_square(Square(8)) | Bitboard.from_square(
                    Square(57)) | Bitboard.from_square(Square(64)),
                queens=Bitboard.from_square(Square(4)) | Bitboard.from_square(Square(60)),
                kings=Bitboard.from_square(Square(5)) | Bitboard.from_square(Square(61)))

    def test_new_game(self):
        self.assertEqual(ChessBitboards.new_game(), self.new_game)

    def test_piece_at(self):
        white: List[Piece] = [Piece.R, Piece.N, Piece.B, Piece.Q, Piece.K, Piece.B, Piece.N, Piece.R]
        black: List[Piece] = [Piece.r, Piece.n, Piece.b, Piece.q, Piece.k, Piece.b, Piece.n, Piece.r]

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
        result = self.new_game.make_move(Move(frm=Square(9), to=Square(17)))

        self.assertFalse(self.new_game == result)
        self.assertIsNone(result.piece_at(Square(9)))
        self.assertEqual(Piece.P, result.piece_at(Square(17)))
        self.assertEqual(self.move_a2_pawn_forward, result)
    #TODO: Test promotions and castling


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
