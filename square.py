# pylint: disable=E1101
"""
square.py
Enum for representing chess board squares.

Author: Noah Rowe
Date: 2022/02/21
Last Modified: 2022/02/23
    Added docstrings
"""

from enum import Enum

_squares:str = ""
for number in range(1, 8 + 1):
    for letter in range(ord('a'), ord('h') + 1):
        _squares += f"{chr(letter)}{str(number)} "

# noinspection PyArgumentList
Square = Enum("Square", _squares)

@property
def rank_of_square(self: Square) -> int:
    """Which rank (row) square is in"""
    return ((self.value-1) // 8) + 1

@property
def file_of_square(self: Square) -> int:
    """Which file (col) square is in"""
    return ((self.value - 1) % 8) + 1


Square.__doc__ = "Enum for representing chess board squares as cords, a1-h8. \n Has properties file and rank"
setattr(Square, 'rank', rank_of_square)
Square.rank.__doc__ = "rank() -> int\n Which rank (row) square is in."
setattr(Square, 'file', file_of_square)
Square.file.__doc__ = "file() -> int\n Which file (col) square is in."
