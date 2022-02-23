# Can't have a low pylint score if you disable all checks. *Taps forehead*
# Disabled because pylint doesn't like the Square class
# Or using "self" as a namedtuple
# pylint: disable=E1101
# pylint: disable=E1136
# pylint: disable= E1133
"""
bitboard_collections.py
NamedTuples holding related bitboards.

Author: Noah Rowe
Date: 2022/02/22
    Was part of bitboards.py
Last Modified: 2022/02/23
    Added docstrings
"""
from __future__ import annotations

from typing import NamedTuple, List

from square import Square
from piece import Piece
from move import Move
from bitboard import Bitboard

class ChessBitboards(NamedTuple):
    """
    ChessBitboards is a NamedTuple subclass.
    Holds bitboards recording piece location for both colors and all chess pieces.
    """
    black: Bitboard
    white: Bitboard
    pawns: Bitboard
    knights: Bitboard
    bishops: Bitboard
    rooks: Bitboard
    queens: Bitboard
    kings: Bitboard

    def piece_at(self:ChessBitboards, square: Square) -> Piece | None:
        """If a piece is at square, return its value, else return None"""
        piece:int = 0
        if self.white & Bitboard.from_square(square):
            piece = 1
        elif self.black & Bitboard.from_square(square):
            piece = -1
        else:
            return None

        for i, board in enumerate(self[2:]):
            if board & Bitboard.from_square(square):
                try:
                    return Piece((i+1) * piece)
                except ValueError:
                    return None

    @classmethod
    def new_game(cls) -> ChessBitboards:
        """Create a new Bitboards representing a new chess game"""
        return cls(
            white=Bitboard.from_rank(1) | Bitboard.from_rank(2),

            black=Bitboard.from_rank(7) | Bitboard.from_rank(8),

            pawns=Bitboard.from_rank(7) | Bitboard.from_rank(2),

            knights=(Bitboard.from_square(Square.b1)
                     | Bitboard.from_square(Square.g1)
                     | Bitboard.from_square(Square.b8)
                     | Bitboard.from_square(Square.g8)),

            bishops=(Bitboard.from_square(Square.c1)
                     | Bitboard.from_square(Square.f1)
                     | Bitboard.from_square(Square.c8)
                     | Bitboard.from_square(Square.f8)),

            rooks=(Bitboard.from_square(Square.a8)
                   | Bitboard.from_square(Square.h8)
                   | Bitboard.from_square(Square.a1)
                   | Bitboard.from_square(Square.h1)),

            queens=(Bitboard.from_square(Square.d4)
                    | Bitboard.from_square(Square.d8)),

            kings=Bitboard.from_square(Square.e8)
                  | Bitboard.from_square(Square.e1)
        )

    def make_move(self:ChessBitboards, move: Move) -> ChessBitboards:
        """Clear move.frm and set move.to in the same bitboard. Clear move.to"""

        if move.promotion_to is None:
            def search(current_bb: Bitboard,
                       frm_mask: Bitboard,
                       to_mask: Bitboard):
                #TODO: Unit test this better
                if current_bb & to_mask:
                    # If the to square is already set in a BB, we're capturing, Therefore clear it
                    current_bb ^= to_mask

                if move.rook_to is not None and current_bb & move.rook_frm:
                    # If there's a rook move, we're castling. Clear frm and set to.
                    current_bb = (current_bb ^ move.rook_frm) | move.rook_to

                if current_bb & frm_mask:
                    # If frm, this is the peice we're moving. Clear it and set to
                    current_bb = (current_bb ^ frm_mask) | to_mask

                return current_bb

            return ChessBitboards(
                    *(search(current_bb,
                             frm_mask=Bitboard.from_square(move.frm),
                             to_mask=Bitboard.from_square(move.to))
                      for current_bb in self))
        else:
            cpy:List[Bitboard] = list(self)
            cpy[2] = self.pawns ^ move.frm
            cpy[abs(move.promotion_to.value)+1] = cpy[abs(move.promotion_to.value)+1]  ^ move.to
            return ChessBitboards(*cpy)


class SpecialMoveBitboards(NamedTuple):
    """
    NamedTuple subclass,
    holding bitboards which are used for determining special move rights.

    Special moves includes castling and ep_rights.
    """
    castling_rooks: Bitboard
    castling_kings: Bitboard
    ep_bitboard: Bitboard

    @property
    def queenside_castling(self):
        """Queenside rooks who are still able to castle"""
        return self.castling_rooks & Bitboard.from_file(1)

    @property
    def kingside_castling(self):
        """Kingside rooks who are still able to castle"""
        return self.castling_rooks & Bitboard.from_file(8)

    @classmethod
    def new_game(cls) -> SpecialMoveBitboards:
        """Alternate constructor for the SpecialMoveBitboards of a new game"""
        return cls(
                castling_rooks= Bitboard.from_square(Square.a1)
                                | Bitboard.from_square(Square.h1)
                                | Bitboard.from_square(Square.a8)
                                | Bitboard.from_square(Square.h8),

                castling_kings=Bitboard.from_square(Square.e1)
                               | Bitboard.from_square(Square.e8),

                ep_bitboard=Bitboard(0)
        )

    def update(self, chess_bitboards:ChessBitboards, move:Move) -> SpecialMoveBitboards:
        """
        Given the current board and the move being made,
        determine the new state of special moves
        """
        ep_sqr:Bitboard = Bitboard(0)
        kings:Bitboard = self.castling_kings
        rooks:Bitboard = self.castling_rooks

        # Test ep squares
        if Bitboard.from_square(move.frm)&chess_bitboards.pawns and (
                (move.frm.rank == 2 and move.to.rank == 4)
                or (move.frm.rank == 7 and move.to.rank == 5)):

            ep_sqr = Bitboard.from_square(
                    Square(((move.frm.rank + move.to.rank) / 2 - 1) * 8 + move.frm.file))

        # Test if kings have moved
        if kings and move.frm in {Square.e1, Square.e8}:
            kings = kings & ~Bitboard.from_square(move.frm)

        # Test if rooks have moved
        if rooks and move.frm in {Square.a1, Square.a8,  Square.h1,  Square.h8}:
            rooks = rooks & ~Bitboard.from_square(move.frm)

        return SpecialMoveBitboards(rooks, kings, ep_sqr)
