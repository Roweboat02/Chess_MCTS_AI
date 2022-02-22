import collections
from collections.abc import Iterable

import bitboards as bb
from bitboards import Bitboard, ChessBitboards
from square import Square
import piece as pce

Move = collections.namedtuple("Move",
                              ["to", "frm"])


def square_distance(a: Square, b: Square) -> int:
    """Rank or file difference (whichever is greater)"""
    return max(abs(a.rank() - b.rank()), abs(a.file() - b.file()))


def sliding_moves(square: Square, occupied: Bitboard, deltas: Iterable[int]) -> Bitboard:
    """
    Repeatedly add a delta to square until resultant is outside bitboard range,
    until resultant wraps around bitboard, or encounters a piece (WILL INCLUDE THAT PIECE)

    bitwise-and with not of color to ensure you're not allowing capturing of colors' own piece.
    """
    moves: Bitboard = Bitboard(0)
    for delta in deltas:
        sqr: Square = square
        while True:
            sqr += delta
            if (0 < sqr <= 64) or square_distance(sqr, sqr - delta) > 2:
                break
            moves |= sqr
            if occupied & Bitboard.from_square(sqr):
                break
    return moves


def step_moves(square: Square, deltas: Iterable[int]) -> Bitboard:
    """Generate bitboard of square+deltas, if resultant is within bitboard range and doesn't wrap board"""
    return bb.reduce_with_bitwise_or(Bitboard.from_square(square + delta)
                                     for delta in deltas
                                     if not (0 < square + delta <= 64)
                                     or 2 >= square_distance(square, square + delta))


def pawn_attacks(square: Square, color: bool) -> Bitboard:
    """
    Possible squares a pawn on @param square of color @param color could attack
    Must be bitwise and'd with all squares occupied by enemy, make sure to include en passents
    """
    return step_moves(square, ((-7, -9), (7, 9))[color])


def knight_moves(square: Square) -> Bitboard:
    """Possible moves a knight on @param square could make"""
    return step_moves(square, (6, -6, 15, -15, 17, -17, 10, -10))


def king_moves(square: Square) -> Bitboard:
    """Possible moves a king on @param square could make"""
    return step_moves(square, (1, -1, 8, -8, 9, -9))


def rank_moves(square: Square, occupied: Bitboard) -> Bitboard:
    """Possible moves a piece which attacks by rank, if it was on @param square"""
    return sliding_moves(square, occupied, (-1, 1))


def file_moves(square: Square, occupied: Bitboard) -> Bitboard:
    """Possible moves a piece which attacks by file, if it was on @param square"""
    return sliding_moves(square, occupied, (-8, 8))


def diagonal_moves(square: Square, occupied: Bitboard) -> Bitboard:
    """Possible moves a piece which attacks by diagonals, if it was on @param square"""
    return sliding_moves(square, occupied, (-9, 9, -7, 7))


def piece_move_mask(square: Square, piece: pce.Piece, occupied: Bitboard) -> Bitboard:
    """
    Possible move @param piece could make if it were on @param square
    Will include the first piece in occupied @param piece will hit. Bitwise or with turn's color bitboard.
    """
    moves: Bitboard = Bitboard(0)
    if abs(piece.value) in {3, 5}:  # Bishop or queen
        moves |= diagonal_moves(square, occupied)
    if abs(piece.value) in {4, 5}:  # Rook or queen
        moves |= rank_moves(square, occupied) | file_moves(square, occupied)
    if abs(piece.value) == 2:  # knight
        moves |= knight_moves(square)
    if abs(piece.value) == 6:  # king
        moves |= king_moves(square)
    return moves
