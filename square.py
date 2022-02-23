from enum import Enum

# For some reason some editors think this is wrong (it isn't)
_squares:str = ""
for number in range(1, 8 + 1):
    for letter in range(ord('a'), ord('h') + 1):
        _squares += f" {chr(letter)}{str(number)}"

Square = Enum("Square", _squares)

@property
def rank_of_square(self: Square) -> int:
    """Which rank (row) square is in"""
    return (self.value // 8) + 1

@property
def file_of_square(self: Square) -> int:
    """Which file (col) square is in"""
    return self.value % 8


setattr(Square, 'rank', rank_of_square)
Square.rank.__doc__ = "rank() -> int\n Which rank (row) square is in"
setattr(Square, 'file', file_of_square)
Square.file.__doc__ = "file() -> int\n Which file (col) square is in"
