from enum import Enum

# For some reason some editors think this is wrong (it isn't)
Square = Enum("Square", [chr(letter) + str(number) for letter in range(ord('a'), ord('h') + 1) for number in range(1, 8 + 1)])


def rank_of_square(self: Square) -> int:
    return self % 8


def file_of_square(self: Square) -> int:
    return self // 8


setattr(Square, 'rank', rank_of_square)
setattr(Square, 'file', file_of_square)
