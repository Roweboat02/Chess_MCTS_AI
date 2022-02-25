# Can't have a low pylint score if you disable all checks. *Taps forehead*
# Disabled because pylint doesn't like the Square class
# Or using "self" as a namedtuple
# pylint: disable=E1136, E1133
"""
special_move_bitboards.py
NamedTuples holding bitboards for special move rights.

Author: Noah Rowe
Date: 2022/02/24
    Was part of chess_bitboards.py
"""
from __future__ import annotations

from typing import NamedTuple

from fog_of_war.square import Square

from fog_of_war.move import Move
from fog_of_war.bitboard import Bitboard
from fog_of_war.chess_bitboards import ChessBitboards


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
    def queen_side_castling(self):
        """Queen side rooks who are still able to castle"""
        return self.castling_rooks & Bitboard.from_file(1)

    @property
    def king_side_castling(self):
        """King side rooks who are still able to castle"""
        return self.castling_rooks & Bitboard.from_file(8)

    @classmethod
    def new_game(cls) -> SpecialMoveBitboards:
        """Alternate constructor for the SpecialMoveBitboards of a new game"""
        return cls(
            castling_rooks=Bitboard.from_square(Square.a1)
                           | Bitboard.from_square(Square.h1)
                           | Bitboard.from_square(Square.a8)
                           | Bitboard.from_square(Square.h8),

            castling_kings=Bitboard.from_square(Square.e1)
                           | Bitboard.from_square(Square.e8),

            ep_bitboard=Bitboard(0)
        )

    def update(self, chess_bitboards: ChessBitboards, move: Move) -> SpecialMoveBitboards:
        """
        Given the current board and the move being made,
        determine the new state of special moves
        """
        ep_sqr: Bitboard = Bitboard(0)
        kings: Bitboard = self.castling_kings
        rooks: Bitboard = self.castling_rooks

        # Test ep squares
        if Bitboard.from_square(move.frm) & chess_bitboards.pawns and (
                (move.frm.rank == 2 and move.to.rank == 4)
                or (move.frm.rank == 7 and move.to.rank == 5)):
            ep_sqr = Bitboard.from_square(
                Square(((move.frm.rank + move.to.rank) / 2 - 1) * 8 + move.frm.file))

        # Test if kings have moved
        if kings and move.frm in {Square.e1, Square.e8}:
            kings = kings & ~Bitboard.from_square(move.frm)

        # Test if rooks have moved
        if rooks:
            if move.rook_frm is not None:
                rooks = rooks & ~Bitboard.from_square(move.rook_frm)
            elif move.frm in {Square.a1, Square.a8, Square.h1, Square.h8}:
                rooks = rooks & ~Bitboard.from_square(move.frm)

        return SpecialMoveBitboards(rooks, kings, ep_sqr)
