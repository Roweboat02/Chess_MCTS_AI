# pylint: disable=C0103
"""
piece.py
Enum for representing chess pieces.

Author: Noah Rowe
Date: 2022/02/21
Last Modified: 2022/02/23
    Added docstrings
"""
import enum


class Piece(enum.Enum):
    """
    Enum representing chess pieces.
    Black pieces are negative and lower-case,
    White pieces are positave and upper-case
    pawn = 1/-1 = P/p
    knight = 2/-2 = N/n
    bishop = 3/-3 = B/b
    rook = 4/-4 = R/r
    queen = 5/-5 = Q/q
    king = 6/-6 = K/k
    """
    P = 1  # White Pawn
    p = -1  # Black Pawn
    N = 2  # White Knight
    n = -2  # Black Knight
    B = 3  # White Bishop
    b = -3  # Black Bishop
    R = 4  # White Rook
    r = -4  # Black Rook
    Q = 5  # White Queen
    q = -5  # Black Queen
    K = 6  # White King
    k = -6  # Black King
