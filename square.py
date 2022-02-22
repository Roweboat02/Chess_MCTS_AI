from enum import Enum

# For some reason some editors think this is wrong (it isn't)
Square = Enum("Square", [chr(letter) + str(number) for number in range(1, 8 + 1) for letter in range(ord('a'), ord('h') + 1) ])


def rank_of_square(self: Square) -> int:
    """Which rank (row) square is in"""
    return (self.value // 8) + 1


def file_of_square(self: Square) -> int:
    """Which file (col) square is in"""
    return self.value % 8


setattr(Square, 'rank', rank_of_square)
setattr(Square, 'file', file_of_square)
