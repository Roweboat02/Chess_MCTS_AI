from functools import reduce

from fog_of_war.square import Square
from random import getrandbits
from fog_of_war.bitboard import Bitboard
from fog_of_war.helper_functions import reverse_scan_for_square

from itertools import chain

def rand_magic():
    return reduce(lambda a, b: a & b, [getrandbits(64) for _ in range(3)])


rook_attack_masks = {sqr: Bitboard.from_rank(sqr.rank) | Bitboard.from_rank(sqr.rank) for sqr in Square}


main_diagonal = Bitboard(0x8040201008040201)
up = ((main_diagonal << 8*i) & 0xFFFF_FFFF_FFFF_FFFF for i in range(1,8))
down = ((main_diagonal >> 8*i) & 0xFFFF_FFFF_FFFF_FFFF for i in range(1,8))
diagonal_attack_masks = {sqr: bb for bb in chain(up, down) for sqr in reverse_scan_for_square(bb)}
# anti_diagonal_attack_masks = {sqr: bb^7 for bb in chain(up, down) for sqr in reverse_scan_for_square(bb^7)}

for key, value in anti_diagonal_attack_masks.items():
    print(key)
    print(Bitboard(value).to_numpy())
