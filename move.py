import collections
from collections.abc import Iterable

import bitboards as bb
import square as sq
import piece as pce

Move = collections.namedtuple("Move",
                              ["to", "frm"])

def make_move(bitboards:bb.Bitboards, move:Move) -> bb.Bitboards:
    """Clear move.frm and set move.to in the same bitboard. Clear move.to"""
    def f(bb: bb.BB, frm_bb: bb.BB, to_bb: bb.BB):
        if bb & frm_bb:
            return (bb ^ frm_bb) | to_bb
        elif bb & to_bb:
            return bb ^ to_bb
        else:
            return bb
    return bb.Bitboards(*[f(bb, bb.BB_square(move.frm), bb.BB_square(move.to)) for bb in bitboards])


def square_distance(a:sq.Square, b:sq.Square) -> int:
    """Rank or file difference (whichever is greater)"""
    return max(abs(sq.rank_of_square(a) - sq.rank_of_square(b)),
               abs(sq.file_of_square(a) - sq.file_of_square(b)))


def sliding_moves(square:sq.Square, occupied: bb.BB, deltas:Iterable[int]) -> bb.BB:
    """
    Repeatedly add a delta to square until resultant is outside bitboard range,
    until resultant wraps around bitboard, or encounters a piece (WILL INCLUDE THAT PIECE)

    bitwise-and with not of color to ensure you're not allowing capturing of colors' own piece.
    """
    moves:bb.BB = bb.BB(0)
    for delta in deltas:
        sqr:sq.Square = square
        while True:
            sqr+=delta
            if (0<sqr<=64) or square_distance(sq, sqr-delta) > 2:
                break
            moves|=sq
            if occupied & bb.BB.BB_square(sqr):
                break
    return moves


def step_moves(square:sq.Square, deltas:Iterable[int]) -> bb.BB:
    """Generate bitboard of square+deltas, if resultant is within bitboard range and doesn't wrap board"""
    return bb.reduce_with_bitwise_or(bb.BB.BB_square(square+delta)
                                  for delta in deltas
                                  if not (0<square+delta<=64)
                                  or 2>=square_distance(square,square+delta))


def pawn_attacks(square:sq.Square, color:bool) -> bb.BB:
    """Must be bitwise and'd with all squares occupied by enemy, make sure to include en passent"""
    return step_moves(square, ((-7, -9), (7, 9))[color])


def pawn_pushes(square:sq.Square, color:bool) -> bb.BB:
    return step_moves(square, ((-1), (1))[color])


def knight_moves(square:sq.Square) -> bb.BB:
    return step_moves(square, (6, -6, 15, -15, 17, -17, 10, -10))


def king_moves(square:sq.Square) -> bb.BB:
    return step_moves(square, (1, -1, 8, -8, 9, -9))


def rank_moves(square:sq.Square, occupied:bb.BB) -> bb.BB:
    return sliding_moves(square, occupied, (-1,1))


def file_moves(square:sq.Square, occupied:bb.BB) -> bb.BB:
    return sliding_moves(square, occupied, (-8,8))


def diagonal_moves(square:sq.Square, occupied:bb.BB) -> bb.BB:
    return sliding_moves(square, occupied, (-9,9,-7,7))


def piece_move_mask(square:sq.Square, piece:pce.Piece, occupied:bb.BB) -> bb.BB:
    moves:bb.BB = bb.BB(0)
    if abs(piece.value) in {3,5}: # Bishop or queen
        moves|=diagonal_moves(square, occupied)
    if abs(piece.value) in {4,5}: # Rook or queen
        moves|=rank_moves(square, occupied)|file_moves(square,occupied)
    if abs(piece.value) == 2: # knight
        moves|=knight_moves(square)
    if abs(piece.value) == 6: # king
        moves |= king_moves(square)
    return moves
