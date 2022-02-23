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
