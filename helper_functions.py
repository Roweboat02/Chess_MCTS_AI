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

from bitboard import Bitboard
from square import Square


def reduce_with_bitwise_or(iterable: Iterable[Bitboard]) -> Bitboard:
    """Bitwise-or all BBs in given iterable. Return resulting bitboard."""
    return Bitboard(reduce(lambda x, y: x | y, iterable))


def reverse_scan_for_piece(bitboard: Bitboard) -> Iterable[Square]:
    """Generator yielding all bit position numbers in the given bitboard."""
    while bitboard:
        length: int = bitboard.bit_length() - 1
        yield length
        bitboard ^= 1 << length
