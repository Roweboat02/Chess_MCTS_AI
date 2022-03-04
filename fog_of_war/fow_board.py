from functools import cached_property
from typing import List

import numpy as np

from fog_of_war.bitboard import Bitboard
from fog_of_war.special_move_bitboards import SpecialMoveBitboards
from fog_of_war.move import Move


class BiasedBoard:
    def __init__(self,
                 numpy_board: np.ndarray,
                 turn: bool,
                 special: SpecialMoveBitboards,
                 visible: Bitboard,
                 possible_moves: List[Move]):
        self.__board: np.ndarray = numpy_board
        self.__turn: bool = turn
        self.__special: SpecialMoveBitboards = special
        self.__visible: Bitboard = visible
        self.__possible_moves: List[Move] = possible_moves

    def apply_fog(self) -> np.ndarray:
        foggy_board: np.ndarray = self.__board.copy()
        foggy_board[np.logical_not(self.visible_to_color)] = 15
        return foggy_board

    @cached_property
    def board(self) -> np.ndarray:
        """Numpy array representation of board, with black on the bottom."""
        # * -1 and mirror about 1 as well if you want it to look like white
        return self.__board if self.__turn else np.flip(self.__board, 0)

    @cached_property
    def visible_to_color(self) -> np.ndarray:
        """Numpy array representation of black's fog, where black is on bottom"""
        vis: np.ndarray = self.__visible.to_numpy()
        return vis if self.__turn else np.flipud(vis)

    @cached_property
    def foggy_board(self) -> np.ndarray:
        """Numpy array representation of board with white's fog applied, where white is on bottom"""
        return self.apply_fog()

