from __future__ import annotations

from typing import NamedTuple

from square import Square
import piece as pce
from move import Move
from bitboard import Bitboard

class ChessBitboards(NamedTuple):
    black: Bitboard
    white: Bitboard
    pawns: Bitboard
    knights: Bitboard
    bishops: Bitboard
    rooks: Bitboard
    queens: Bitboard
    kings: Bitboard

    def piece_at(self, square: Square) -> pce.Piece | None:
        """If a piece is at square, return its value, else return None"""
        if self.white & Bitboard.from_square(square):
            piece = 1
        elif self.black & Bitboard.from_square(square):
            piece = -1
        else:
            return None

        for i, bb in enumerate(self[2:]):
            if bb & Bitboard.from_square(square):
                try:
                    return pce.Piece((i+1) * piece)
                except ValueError:
                    return None

    @classmethod
    def new_game(cls) -> ChessBitboards:
        """Create a new Bitboards representing a new chess game"""
        return cls(
            white=Bitboard.from_rank(1) | Bitboard.from_rank(2),
            black=Bitboard.from_rank(7) | Bitboard.from_rank(8),
            pawns=Bitboard.from_rank(7) | Bitboard.from_rank(2),
            knights=Bitboard.from_square(Square(2)) | Bitboard.from_square(Square(7)) | Bitboard.from_square(Square(58)) | Bitboard.from_square(Square(63)),
            bishops=Bitboard.from_square(Square(3)) | Bitboard.from_square(Square(6)) | Bitboard.from_square(Square(59)) | Bitboard.from_square(Square(62)),
            rooks=Bitboard.from_square(Square(1)) | Bitboard.from_square(Square(8)) | Bitboard.from_square(Square(57)) | Bitboard.from_square(Square(64)),
            queens=Bitboard.from_square(Square(4)) | Bitboard.from_square(Square(60)),
            kings=Bitboard.from_square(Square(5)) | Bitboard.from_square(Square(61))
        )

    def make_move(self, move: Move) -> ChessBitboards:
        """Clear move.frm and set move.to in the same bitboard. Clear move.to"""

        def f(current_bb: Bitboard, frm_bb: Bitboard, to_bb: Bitboard):
            if current_bb & frm_bb:
                return (current_bb ^ frm_bb) | to_bb
            elif current_bb & to_bb:
                return current_bb ^ to_bb
            else:
                return current_bb

        return ChessBitboards(*[f(current_bb, Bitboard.from_square(move.frm), Bitboard.from_square(move.to))
                                for current_bb in self])

class SpecialMoveBitboards(NamedTuple):
    castling_rooks: Bitboard
    castling_kings: Bitboard
    ep_bitboard: Bitboard

    @property
    def queenside_castling(self):
        return self.castling_rooks & Bitboard.from_file(1)

    @property
    def kingside_castling(self):
        return self.castling_rooks & Bitboard.from_file(8)

    @classmethod
    def new_game(cls) -> SpecialMoveBitboards:
        """Alternate constructor for the SpecialMoveBitboards of a new game"""
        return cls(
                Bitboard.from_square(Square(1)) | Bitboard.from_square(Square(8)) | Bitboard.from_square(Square(57)) | Bitboard.from_square(Square(64)),
                Bitboard.from_square(Square(5)) | Bitboard.from_square(Square(61)),
                Bitboard(0))

    def update(self, chess_bitboards:ChessBitboards, move:Move) -> SpecialMoveBitboards:
        """Given the current board and the move being made, and determine the new state of special moves"""
        ep:Bitboard = Bitboard(0)
        kings:Bitboard = self.castling_kings
        rooks:Bitboard = self.castling_rooks

        # Test ep squares
        if ((move.frm.rank() == 2 and move.to.rank() == 4) or (move.frm.rank() == 7 and move.to.rank() == 5)) and Bitboard.from_square(move.frm)&chess_bitboards.pawns:
            ep = Bitboard.from_square( Square( ((move.frm.rank() + move.to.rank()) / 2 - 1) * 8 + move.frm.file()))

        # Test if kings have moved
        if kings and (move.frm==Square(5) or move.frm==Square(61)):
            kings = kings & ~Bitboard.from_square(move.frm)

        # Test if rooks have moved
        if rooks and (move.frm==Square(1) or move.frm==Square(8) or move.frm==Square(57) or move.frm==Square(64)):
            rooks = rooks & ~Bitboard.from_square(move.frm)

        return SpecialMoveBitboards(rooks, kings, ep)
