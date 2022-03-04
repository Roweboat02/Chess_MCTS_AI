"""
attack_masks.py
Functions for generating bitboard masks for different pieces attack patterns.

Author: Noah Rowe
Date: 2022/02/22
Last Modified: 2022/02/23
    Added docstrings
"""
from typing import Iterable

from fog_of_war.bitboard import Bitboard
from fog_of_war.helper_functions import reduce_with_bitwise_or
from fog_of_war.piece import Piece
from fog_of_war.square import Square


def _square_distance(square_a: Square, square_b: Square) -> int:
    """Rank or file difference (whichever is greater)"""
    return max(abs(square_a.rank - square_b.rank), abs(square_a.file - square_b.file))


def _find_possible_sliding_moves(square: Square, occupied: Bitboard, deltas: Iterable[int]) -> Bitboard:
    """
    Repeatedly add a delta to square until resultant is outside bitboard range,
    until resultant wraps around bitboard, or encounters a piece (WILL INCLUDE THAT PIECE)

    bitwise-and with not of color to ensure you're not allowing capturing of colors' own piece.
    """
    moves: Bitboard = Bitboard(0)
    for delta in deltas:
        sqr: int = square.value
        while True:
            sqr += delta
            if not (0 < sqr <= 64) or (_square_distance(Square(sqr), Square(sqr - delta)) > 2):
                break
            moves |= Bitboard.from_square(Square(sqr))
            if occupied & Bitboard.from_square(Square(sqr)):
                break
    return moves


def _single_step_moves(square: Square, deltas: Iterable[int]) -> Bitboard:
    """
    Generate bitboard of square+deltas, if resultant is within bitboard range and doesn't wrap board
    """
    return reduce_with_bitwise_or(*(Bitboard.from_square(Square(square.value + delta))
                                  if (0 < square.value + delta <= 64)
                                     and 2 >= _square_distance(square, Square(square.value + delta))
                                  else Bitboard(0)
                                  for delta in deltas))


def pawn_attack_mask(square: Square, color: bool) -> Bitboard:
    """
    Possible squares a pawn on @param square of @param color could attack
    Must be bitwise and'd with all squares occupied by enemy, make sure to include en passents
    """
    return _single_step_moves(square, ((-7, -9), (7, 9))[color])


def knight_moves(square: Square) -> Bitboard:
    """Possible moves a knight on @param square could make"""
    return _single_step_moves(square, (6, -6, 15, -15, 17, -17, 10, -10))


def king_moves(square: Square) -> Bitboard:
    """Possible moves a king on @param square could make"""
    return _single_step_moves(square, (1, -1, 8, -8, 9, -9, 7, -7))


def rank_moves(square: Square, occupied: Bitboard) -> Bitboard:
    """Possible moves a piece which attacks by rank, if it was on @param square"""
    return _find_possible_sliding_moves(square, occupied, (-1, 1))


def file_moves(square: Square, occupied: Bitboard) -> Bitboard:
    """Possible moves a piece which attacks by file, if it was on @param square"""
    return _find_possible_sliding_moves(square, occupied, (-8, 8))


def diagonal_moves(square: Square, occupied: Bitboard) -> Bitboard:
    """Possible moves a piece which attacks by diagonals, if it was on @param square"""
    return _find_possible_sliding_moves(square, occupied, (-9, 9, -7, 7))


def non_pawn_move_mask(square: Square, piece: Piece, occupied: Bitboard) -> Bitboard:
    """
    Possible move @param piece could make if it were on @param square

    Does not work for pawns
    Will include the first piece in @param occupied @param piece will hit.
    Bitwise or with turn's color bitboard.
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
