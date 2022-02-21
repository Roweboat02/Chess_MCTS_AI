import enum

Square = enum.Enum([chr(letter) + str(number)
                    for letter in range(ord('a'), ord('h') + 1)
                    for number in range(1, 8 + 1)])


def rank_of_square(square: Square) -> int:
    return square % 8


def file_of_square(square: Square) -> int:
    return square // 8
