from collections.abc import Iterator, Iterable
from __future__ import annotations
from functools import reduce
from typing import NamedTuple

import numpy as np

import square as sq
import piece as pce

class BB(int):
    def __init__(self, bb:int):
        assert(bb.bit_length() <= 64, "Must be able to be represented as 64 bit")
        assert(bb > -1, "Must be positave")
        super(bb)

    @classmethod
    def BB_rank(cls, rankNum: int) -> BB:
        """
        Create a bitboard with the specified rank set to 1.
        @param rankNum:int - interger between 1 and 8 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with rank (row) rankNum 1, and all else 0.
        """
        return cls(0b11111111 << (rankNum - 1) * 8)

    @classmethod
    def BB_file(cls, fileNum: int) -> BB:
        """
        Create a bitboard with the specified file set to 1.
        @param fileNum:int - interger between 1 and 8 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with file (col) fileNum 1, and all else 0.
        """
        return cls(0x0101_0101_0101_0101 << (fileNum - 1) * 8)

    @classmethod
    def BB_square(cls, squareNum: sq.Square) -> BB:
        """
        Create a bitboard with the specified square set to 1, numbered rank*8 + file.
        @param squareNum:Square - item from enum Square used as an int between 1 and 64 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with square squareNum, and all else 0.
        """
        return cls(1 << (squareNum - 1))


class Bitboards(NamedTuple):
    black:BB
    white:BB
    pawns:BB
    knights:BB
    bishops:BB
    rooks:BB
    queens:BB
    kings:BB

    def piece_at(self, square:sq.Square)->pce.Piece|None:
        if self.white & BB.BB_square(square):
            piece = 1
        elif self.black & BB.BB_square(square):
            piece = -1
        else:
            return None

        for i, bb in enumerate(self[2:]):
            if bb & BB.BB_square(square):
                return pce.Piece(i*piece)

    @classmethod
    def new_game(cls) -> Bitboards:
        return cls(
                white=BB.BB_rank(1) | BB.BB_rank(2),
                black=BB.BB_rank(7) | BB.BB_rank(8),
                pawns=BB.BB_rank(7) | BB.BB_rank(2),
                knights=BB.BB_square(3) | BB.BB_square(6) | BB.BB_square(58) | BB.BB_square(62),
                bishops=BB.BB_square(2) | BB.BB_square(7) | BB.BB_square(57) | BB.BB_square(63),
                rooks=BB.BB_square(1) | BB.BB_square(8) | BB.BB_square(56) | BB.BB_square(64),
                queens=BB.BB_square(4) | BB.BB_square(60),
                kings=BB.BB_square(5) | BB.BB_square(61)
        )


def reduce_with_bitwise_or(iterable:Iterable[BB]) -> BB:
    """Bitwise-or all BBs in given iterable. Return resulting bitboard."""
    return BB(reduce(lambda x, y: x | y, iterable))


def reverse_scan_for_piece(bitboard:BB) -> Iterator[sq.Square]:
    """Generator yielding all bit position numbers in the given bitboard."""
    while bitboard:
        length:int = bitboard.bit_length()-1
        yield length
        bitboard ^= 1<<length

def bitboard_to_numpy(bb:BB) -> np.ndarray:
    """
    Convert bitboard from int representation to representing as a numpy array of 1's and 0's
    @return arr:np.ndarray - An 8x8 numpy array (dtype=np.int16)
    """
    return np.unpackbits((bb >> np.arange(0, 57, 8)).astype(np.uint8), bitorder="little").reshape(8, 8).astype(
        np.int16)
