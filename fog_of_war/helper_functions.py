"""
helper_functions.py
File for general functions.

Author: Noah Rowe
Date: 2022/02/22
    Functions were in various files before
Last Modified: 2022/02/23
    Added docstrings
"""
from collections.abc import Iterable
from functools import reduce

from fog_of_war.bitboard import Bitboard
from fog_of_war.square import Square


def reduce_with_bitwise_or(*args: Bitboard) -> Bitboard:
    """Bitwise-or all BBs in given iterable. Return resulting bitboard."""
    try:
        return Bitboard(reduce(lambda x, y: x | y, args))
    except TypeError:
        return Bitboard(0)


def reverse_scan_for_square(bitboard: Bitboard) -> Iterable[Square]:
    """Generator yielding all bit position numbers in the given bitboard."""
    while bitboard:
        length: int = bitboard.bit_length()
        yield Square(length)
        bitboard ^= 1 << (length-1)
