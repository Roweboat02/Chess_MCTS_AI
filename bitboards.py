import collections
from collections.abc import Iterator, Iterable
from functools import reduce
from typing import List

import numpy as np

from piece import Piece
from square import Square
import square as sq

Bitboards = collections.namedtuple("Bitboards",
                                   ["white", "black", "pawns", "knights", "bishops", "rooks", "queens", "kings"])

def BB_rank(num:int) -> int:
    return 0b11111111 << (num-1)*8


def BB_file(num:int) -> int:
    return 0x0101_0101_0101_0101 << (num-1)*8


def BB_square(num:int) -> int:
    return 1<<(num-1)


def bitboard_to_numpy(bb):
    s = 8 * np.arange(7, -1, -1, dtype=np.uint8)
    return np.unpackbits((bb >> s).astype(np.uint8), bitorder="little").reshape(8, 8)


def reduce_with_bitwise_or(iterable:Iterable[int]) -> int:
    return reduce(lambda x, y: x | y, iterable)


def reverse_scan_for_peice(bitboard:int) -> Iterator[int]:
    while bitboard:
        length = bitboard.bit_length()-1
        yield length
        bitboard ^= 1<<length


def bb_to_numpy(bb: int)->np.ndarray:
    return np.unpackbits((bb>>np.arange(0, 57, 8)).astype(np.uint8), bitorder="little").reshape(8, 8).astype(np.int16)


def sliding_attacks(square:Square, deltas:Iterable[int])->int:  # Prob split off the max(...) into it's own function at some point
    return reduce_with_bitwise_or(square+delta
                                  for delta in deltas
                                  if not (0<square+delta<=64)
                                  or 2>=max(abs(sq.rank_of_square(square)-sq.rank_of_square(square+delta)),
                                            abs(sq.file_of_square(square)-sq.file_of_square(square+delta))))


def pawn_attacks(square:Square, color:bool)->int:
    return sliding_attacks(square, ((-7,-9),(7,9))[color])


def rank_attacks(square:Square)->int:
    return BB_rank(sq.rank_of_square(square))


def file_attacks(square:Square)->int:
    return BB_file(sq.file_of_square(square))


def diagonal_attacks(square:Square)->int: pass # TODO: implement


def attack_masks(square: Square, piece:Piece)->int:
    return {
            # Literally made these up as I done them. There's actual lists on chess programming wiki.
            # TODO: need to add check if peices wrap around board
            Piece.p: lambda sq: BB_square(sq - 7) | BB_square(sq - 9),
            Piece.P: lambda sq: BB_square(sq + 7) | BB_square(sq + 9),

            Piece.k: lambda sq: reduce_with_bitwise_or(map(lambda i: BB_square(i+sq), (-7, -8, -9, -1, 1, 7, 8, 9))),
            Piece.K: lambda sq: reduce_with_bitwise_or(map(lambda i: BB_square(i+sq), (-7, -8, -9, -1, 1, 7, 8, 9))),

            Piece.N: lambda sq: reduce_with_bitwise_or(map(lambda i: BB_square(i+sq), (6, -6, 15, -15, 17, -17, 10, -10))),
            Piece.n: lambda sq: reduce_with_bitwise_or(map(lambda i: BB_square(i+sq), (6, -6, 15, -15, 17, -17, 10, -10))),

            Piece.Q: lambda sq: rank_attacks(sq) | file_attacks(sq) | diagonal_attacks(sq),
            Piece.q: lambda sq: rank_attacks(sq) | file_attacks(sq) | diagonal_attacks(sq),

            Piece.R: lambda sq: rank_attacks(sq) | file_attacks(sq),
            Piece.r: lambda sq: rank_attacks(sq) | file_attacks(sq),

            Piece.B: lambda sq: diagonal_attacks(sq),
            Piece.b: lambda sq: diagonal_attacks(sq),
    }[piece](square)
