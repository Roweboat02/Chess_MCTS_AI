from collections.abc import Iterator, Iterable
from functools import reduce
from typing import NamedTuple

import numpy as np

import move as mv
import piece as pce
import square as sq


class BB(int):
    def __init__(self, bb:int):
        assert(bb.bit_length() <= 64, "Must be able to be represented as 64 bit")
        assert(bb > -1, "Must be positave")
        super(bb)


class Bitboards(NamedTuple):
    black:BB
    white:BB
    pawns:BB
    knights:BB
    bishops:BB
    rooks:BB
    queens:BB
    kings:BB

def make_move(bitboards:Bitboards, move:mv.Move)->Bitboards:
    """Clear move.frm and set move.to in the same bitboard. Clear move.frm"""
    def f(bb: BB, frm_bb: BB, to_bb: BB):
        if bb & frm_bb:
            return (bb ^ frm_bb) | to_bb
        elif bb & to_bb:
            return bb ^ to_bb
        else:
            return bb
    return Bitboards(*[f(bb, BB_square(move.frm), BB_square(move.to)) for bb in bitboards])

def BB_rank(rankNum:int) -> BB:
    """
    Create a bitboard with the specified rank set to 1.
    @param rankNum:int - interger between 1 and 8 (inclusive)
    @return bb:int - int that can be interpreted as an 8x8 bitboard with rank (row) rankNum 1, and all else 0.
    """
    return BB(0b11111111 << (rankNum - 1) * 8)


def BB_file(fileNum:int) -> BB:
    """
    Create a bitboard with the specified file set to 1.
    @param fileNum:int - interger between 1 and 8 (inclusive)
    @return bb:int - int that can be interpreted as an 8x8 bitboard with file (col) fileNum 1, and all else 0.
    """
    return BB(0x0101_0101_0101_0101 << (fileNum-1)*8)


def BB_square(squareNum:sq.Square) -> BB:
    """
    Create a bitboard with the specified square set to 1, numbered rank*8 + file.
    @param squareNum:Square - item from enum Square used as an int between 1 and 64 (inclusive)
    @return bb:int - int that can be interpreted as an 8x8 bitboard with square squareNum, and all else 0.
    """
    return BB(1<<(squareNum-1))


def reduce_with_bitwise_or(iterable:Iterable[BB]) -> BB:
    """Bitwise-or all BBs in given iterable. Return resulting bitboard."""
    return BB(reduce(lambda x, y: x | y, iterable))


def reverse_scan_for_peice(bitboard:BB) -> Iterator[sq.Square]:
    """Generator yielding all bit position numbers in the given bitboard."""
    while bitboard:
        length:int = bitboard.bit_length()-1
        yield length
        bitboard ^= 1<<length


def bitboard_to_numpy(bb: BB)->np.ndarray:
    """
    Convert bitboard from int representation to representing as a numpy array of 1's and 0's
    @param bb:BB - An int that must be a positave and can be represented as 64 bits.
    @return arr:np.ndarray - An 8x8 numpy array (dtype=np.int16)
    """
    return np.unpackbits((bb>>np.arange(0, 57, 8)).astype(np.uint8), bitorder="little").reshape(8, 8).astype(np.int16)


def sliding_attacks(square:sq.Square, deltas:Iterable[int])->BB:  # Prob split off the max(...) into it's own function at some point
    """"""
    return reduce_with_bitwise_or(BB_square(square+delta)
                                  for delta in deltas
                                  if not (0<square+delta<=64)
                                  or 2>=max(abs(sq.rank_of_square(square)-sq.rank_of_square(square+delta)),
                                            abs(sq.file_of_square(square)-sq.file_of_square(square+delta))))


def pawn_attacks(square:sq.Square, color:bool)->BB:
    return sliding_attacks(square, ((-7,-9),(7,9))[color])


def rank_attacks(square:sq.Square)->BB:
    return BB_rank(sq.rank_of_square(square))


def file_attacks(square:sq.Square)->BB:
    return BB_file(sq.file_of_square(square))


def diagonal_attacks(square:sq.Square)->BB: pass # TODO: implement


def attack_masks(square: sq.Square, piece:pce.Piece)->BB:
    return {
            # Literally made these up as I done them. There's actual lists on chess programming wiki.
            # TODO: need to add check if peices wrap around board
            pce.Piece.p: lambda sq: BB_square(sq - 7) | BB_square(sq - 9),
            pce.Piece.P: lambda sq: BB_square(sq + 7) | BB_square(sq + 9),

            pce.Piece.k: lambda sq: reduce_with_bitwise_or(map(lambda i: BB_square(i+sq), (-7, -8, -9, -1, 1, 7, 8, 9))),
            pce.Piece.K: lambda sq: reduce_with_bitwise_or(map(lambda i: BB_square(i+sq), (-7, -8, -9, -1, 1, 7, 8, 9))),

            pce.Piece.N: lambda sq: reduce_with_bitwise_or(map(lambda i: BB_square(i+sq), (6, -6, 15, -15, 17, -17, 10, -10))),
            pce.Piece.n: lambda sq: reduce_with_bitwise_or(map(lambda i: BB_square(i+sq), (6, -6, 15, -15, 17, -17, 10, -10))),

            pce.Piece.Q: lambda sq: rank_attacks(sq) | file_attacks(sq) | diagonal_attacks(sq),
            pce.Piece.q: lambda sq: rank_attacks(sq) | file_attacks(sq) | diagonal_attacks(sq),

            pce.Piece.R: lambda sq: rank_attacks(sq) | file_attacks(sq),
            pce.Piece.r: lambda sq: rank_attacks(sq) | file_attacks(sq),

            pce.Piece.B: lambda sq: diagonal_attacks(sq),
            pce.Piece.b: lambda sq: diagonal_attacks(sq),
    }[piece](square)

def NewGameBitboards():
    return Bitboards(
    white = BB_rank(1) | BB_rank(2),
    black = BB_rank(7) | BB_rank(8),
    pawns = BB_rank(7) | BB_rank(2),
    knights = BB_square(3) | BB_square(6) | BB_square(58) | BB_square(62),
    bishops = BB_square(2) | BB_square(7) | BB_square(57) | BB_square(63),
    rooks = BB_square(1) | BB_square(8) | BB_square(56) | BB_square(64),
    queens = BB_square(4) | BB_square(60),
    kings = BB_square(5) | BB_square(61)
    )
