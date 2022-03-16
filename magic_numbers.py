from functools import reduce

from fog_of_war.square import Square
from random import getrandbits
from fog_of_war.bitboard import Bitboard
from fog_of_war.helper_functions import reverse_scan_for_square

from itertools import chain


def rand_magic():
    return reduce(lambda a, b: a & b, [getrandbits(64) for _ in range(3)])


rook_attack_masks = {sqr: Bitboard.from_rank(sqr.rank) | Bitboard.from_rank(sqr.rank) for sqr in Square}

diagonal_attack_dicts = []
main_diagonal = 0x8040201008040201
main_anti_diagonal = 0x102040810204080


def diag_getter(diag):
    up = ((diag << 8 * i) & 0xFFFF_FFFF_FFFF_FFFF for i in range(1, 8))
    down = ((diag >> 8 * i) & 0xFFFF_FFFF_FFFF_FFFF for i in range(1, 8))
    return {sqr: bb for bb in chain(up, down, [diag]) for sqr in reverse_scan_for_square(bb)}


a = diag_getter(main_anti_diagonal)
print(list(a.keys())==list(set(a.keys())))

# bishop_attack_masks = {
#     square: (diag_getter(main_diagonal)[square] | diag_getter(main_anti_diagonal)[square]) for square in Square}
#
# print(bishop_attack_masks)
