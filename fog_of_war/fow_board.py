from __future__ import annotations

from functools import cached_property
from typing import List

import numpy as np
from fog_of_war.piece import Piece
from fog_of_war.square import Square
from fog_of_war.chess_bitboards import ChessBitboards
from fog_of_war.fog_of_war_chess import FOWChess
from fog_of_war.bitboard import Bitboard
from fog_of_war.move import Move


def _apply_fog(board: np.ndarray, visible: np.ndarray) -> np.ndarray:
    foggy_board: np.ndarray = board.copy()
    foggy_board[np.logical_not(visible)] = 15
    return foggy_board


class FOWBoard:
    def __init__(self,
                 bitboards: ChessBitboards,
                 turn: bool,
                 visible: Bitboard,
                 possible_moves: List[Move]):
        numpy_board: np.ndarray = bitboards.to_numpy()
        board: np.ndarray = numpy_board if turn else np.flip(numpy_board, 0)

        vis: np.ndarray = visible.to_numpy()
        self.__visible: np.ndarray = vis if turn else np.flipud(vis)

        self.__foggy_board: np.ndarray = _apply_fog(board, self.__visible)

        self.__turn: bool = turn
        self.__possible_moves: List[Move] = possible_moves

    @classmethod
    def from_fow_chess(cls, fow: FOWChess, turn: bool) -> FOWBoard:
        """
        I'm not sure how I want to handle creation yet.
        This is just acting as a place holder,
        I don't like that I'm giving the complete game state to the incomplete
        game state.
        """
        bitboards: ChessBitboards = fow.bitboards
        visible: Bitboard = fow._visible_squares(turn)  # private method here because of above comment
        moves: List[Move] = fow.possible_moves_list if turn == fow.current_turn else []
        return cls(bitboards, turn, visible, moves)

    def __getitem__(self, key: Square) -> Piece:
        return self.__foggy_board[7 - key.rank, 7 - key.file]

    @property
    def foggy_board(self) -> np.ndarray:
        """Numpy array representation of board, with black on the bottom."""
        # * -1 and mirror about 1 as well if you want it to look like white
        return self.__foggy_board

    @property
    def visible_to_color(self) -> np.ndarray:
        """Numpy array representation of black's fog, where black is on bottom"""
        return self.__visible

    @property
    def turn(self) -> bool:
        """The player FOWBoard is in the persprective of"""
        return self.__turn
