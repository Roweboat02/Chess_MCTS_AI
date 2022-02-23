"""
move.py
Dataclass for representing moves in a chess game

Author: Noah Rowe
Date: 2022/02/21
Last Modified: 2022/02/23
    Added docstrings
"""
from dataclasses import dataclass
from typing import Optional

from square import Square
from piece import Piece

@dataclass
class Move:
    """
    Use to and frm to specify a chess move.

    If move is a promotion,
     make to and frm equal,
     and specify the Piece promotion_to (None by default)
     assumes is promoted from pawn as that's the only legal promotion in chess

    If move is castling,
     make to and frm the squares the king moves to /from
     specify where the rook moves to and from using rook_to and rook_frm
     (both rook_to and rook_frm are None by default)
    """
    to:Square
    frm:Square
    rook_to: Optional[Square] = None
    rook_frm: Optional[Square] = None
    promotion_to: Optional[Piece] = None
