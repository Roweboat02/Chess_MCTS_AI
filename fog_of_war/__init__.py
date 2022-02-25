"""
The fog of war package contains:

chess data representations:
bitboards,
moves,
board squares,
chess pieces

Collections of bitboards for:
Pieces and colors,
special moves

The above classes are used to make a fog of war class, which holds a fog of war game state.
"""
from fog_of_war.attack_masks import *
from fog_of_war.bitboard import Bitboard
from fog_of_war.chess_bitboards import ChessBitboards
from fog_of_war.special_move_bitboards import SpecialMoveBitboards
from fog_of_war.move import Move
from fog_of_war.piece import Piece
from fog_of_war.square import Square
