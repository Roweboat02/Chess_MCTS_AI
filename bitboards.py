from __future__ import annotations

from collections.abc import Iterator, Iterable
from functools import reduce
from typing import NamedTuple

import numpy as np

import square as sq
import piece as pce
from move import Move

def reduce_with_bitwise_or(iterable: Iterable[Bitboard]) -> Bitboard:
    """Bitwise-or all BBs in given iterable. Return resulting bitboard."""
    return Bitboard(reduce(lambda x, y: x | y, iterable))


def reverse_scan_for_piece(bitboard: Bitboard) -> Iterator[sq.Square]:
    """Generator yielding all bit position numbers in the given bitboard."""
    while bitboard:
        length: int = bitboard.bit_length() - 1
        yield length
        bitboard ^= 1 << length


class Bitboard(int):
    # TODO: add more methods so results are also Bitboard https://stackoverflow.com/a/46196226
    # Also look into better ways to subclass builtins
    # Also make alternative consturctors use main constructor so asserts (which should be errors prob) are checked

    def __new__(cls, bb: int):
        if not (bb.bit_length() <= 64 or bb > -1):
            raise ValueError("Must be a positave interger representable as 64 bits")
        return super(Bitboard, cls).__new__(cls, bb)

    def bitboard_to_numpy(self) -> np.ndarray:
        """
        Convert bitboard from int representation to representing as a numpy array of 1's and 0's
        @return arr:np.ndarray - An 8x8 numpy array (dtype=np.int16)
        """
        return np.flipud(np.unpackbits((int(self) >> np.arange(0, 57, 8, dtype=np.uint8)).astype(np.uint8), bitorder="little").reshape(8, 8).astype(np.int16))

    @classmethod
    def from_rank(cls, rank_num: int) -> Bitboard:
        """
        Create a bitboard with the specified rank set to 1.
        @param rank_num:int - integer between 1 and 8 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with rank (row) rankNum 1, and all else 0.
        """
        if not 0<rank_num<9:
            raise ValueError
        return cls(0b11111111 << (rank_num - 1) * 8)

    @classmethod
    def from_file(cls, file_num: int) -> Bitboard:
        """
        Create a bitboard with the specified file set to 1.
        @param file_num:int - integer between 1 and 8 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with file (col) fileNum 1, and all else 0.
        """
        if not 0<file_num<9:
            raise ValueError
        return cls(0x0101_0101_0101_0101 << (file_num - 1) * 8)

    @classmethod
    def from_square(cls, square_num: sq.Square) -> Bitboard:
        """
        Create a bitboard with the specified square set to 1, numbered rank*8 + file.
        @param square_num:Square - item from enum Square used as an int between 1 and 64 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with square squareNum, and all else 0.
        """
        return cls(1 << (square_num - 1))


class ChessBitboards(NamedTuple):
    black: Bitboard
    white: Bitboard
    pawns: Bitboard
    knights: Bitboard
    bishops: Bitboard
    rooks: Bitboard
    queens: Bitboard
    kings: Bitboard

    def piece_at(self, square: sq.Square) -> pce.Piece | None:
        """If a piece is at square, return its value, else return None"""
        if self.white & Bitboard.from_square(square):
            piece = 1
        elif self.black & Bitboard.from_square(square):
            piece = -1
        else:
            return None

        for i, bb in enumerate(self[2:]):
            if bb & Bitboard.from_square(square):
                return pce.Piece(i * piece)

    @classmethod
    def new_game(cls) -> ChessBitboards:
        """Create a new Bitboards representing a new chess game"""
        return cls(
            white=Bitboard.from_rank(1) | Bitboard.from_rank(2),
            black=Bitboard.from_rank(7) | Bitboard.from_rank(8),
            pawns=Bitboard.from_rank(7) | Bitboard.from_rank(2),
            knights=Bitboard.from_square(3) | Bitboard.from_square(6) | Bitboard.from_square(58) | Bitboard.from_square(
                62),
            bishops=Bitboard.from_square(2) | Bitboard.from_square(7) | Bitboard.from_square(57) | Bitboard.from_square(
                63),
            rooks=Bitboard.from_square(1) | Bitboard.from_square(8) | Bitboard.from_square(56) | Bitboard.from_square(
                64),
            queens=Bitboard.from_square(4) | Bitboard.from_square(60),
            kings=Bitboard.from_square(5) | Bitboard.from_square(61)
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
    ep_squares: Bitboard

    # @classmethod
    # def new_game(cls) -> SpecialMoveBitboards:
    #     return cls(
    #             0x81 | 0x81<<56,
    #
    #                )
