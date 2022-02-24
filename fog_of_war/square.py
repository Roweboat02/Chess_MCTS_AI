# pylint: disable=C0103
"""
square.py
Enum for representing chess board squares.

Author: Noah Rowe
Date: 2022/02/21
Last Modified: 2022/02/23
    Added docstrings
"""
from __future__ import annotations
from enum import Enum, auto


class Square(Enum):
    """
    Enum for representing chess board squares as cords, a1-h8.
    Has properties file and rank
    """
    a1 = auto()
    b1 = auto()
    c1 = auto()
    d1 = auto()
    e1 = auto()
    f1 = auto()
    g1 = auto()
    h1 = auto()
    a2 = auto()
    b2 = auto()
    c2 = auto()
    d2 = auto()
    e2 = auto()
    f2 = auto()
    g2 = auto()
    h2 = auto()
    a3 = auto()
    b3 = auto()
    c3 = auto()
    d3 = auto()
    e3 = auto()
    f3 = auto()
    g3 = auto()
    h3 = auto()
    a4 = auto()
    b4 = auto()
    c4 = auto()
    d4 = auto()
    e4 = auto()
    f4 = auto()
    g4 = auto()
    h4 = auto()
    a5 = auto()
    b5 = auto()
    c5 = auto()
    d5 = auto()
    e5 = auto()
    f5 = auto()
    g5 = auto()
    h5 = auto()
    a6 = auto()
    b6 = auto()
    c6 = auto()
    d6 = auto()
    e6 = auto()
    f6 = auto()
    g6 = auto()
    h6 = auto()
    a7 = auto()
    b7 = auto()
    c7 = auto()
    d7 = auto()
    e7 = auto()
    f7 = auto()
    g7 = auto()
    h7 = auto()
    a8 = auto()
    b8 = auto()
    c8 = auto()
    d8 = auto()
    e8 = auto()
    f8 = auto()
    g8 = auto()
    h8 = auto()

    @property
    def rank(self: Square) -> int:
        """Which rank (row) square is in"""
        return ((self.value - 1) // 8) + 1

    @property
    def file(self: Square) -> int:
        """Which file (col) square is in"""
        return ((self.value - 1) % 8) + 1

# Didn't want to type out chess cords, but type checker didn't like that much.
# Thank god for macros

# _squares:str = ""
# for number in range(1, 8 + 1):
#     for letter in range(ord('a'), ord('h') + 1):
#         _squares += f"{chr(letter)}{str(number)} "
#
# Square = Enum("Square", _squares)
# Square.__doc__ =
# "Enum for representing chess board squares as cords, a1-h8. \n Has properties file and rank"
# setattr(Square, 'rank', rank_of_square)
# Square.rank.__doc__ = "rank([]) -> int\n Which rank (row) square is in."
# setattr(Square, 'file', file_of_square)
# Square.file.__doc__ = "file([]) -> int\n Which file (col) square is in."
