from __future__ import annotations

from typing import List

import numpy as np

import bitboards as bb
import move as mv
import piece as pce


class FOWChess:
    WHITE = True
    BLACK = False

    def __init__(self, bitboards:bb.Bitboards) -> None:
        self._bitboards = bitboards

    @classmethod
    def new_game(cls) -> FOWChess:
        a = cls(bb.Bitboards(0, 0, 0, 0, 0, 0, 0, 0))
        a._reset_board()
        return a

    def _reset_board(self) -> None:
        self._bitboards.white = bb.BB_rank(1) | bb.BB_rank(2)
        self._bitboards.black = bb.BB_rank(7) | bb.BB_rank(8)
        self._bitboards.pawns = bb.BB_rank(7) | bb.BB_rank(2)
        self._bitboards.bishops = bb.BB_square(3) | bb.BB_square(6) | bb.BB_square(58) | bb.BB_square(62)
        self._bitboards.knights = bb.BB_square(2) | bb.BB_square(7) | bb.BB_square(57) | bb.BB_square(63)
        self._bitboards.rook = bb.BB_square(1) | bb.BB_square(8) | bb.BB_square(56) | bb.BB_square(64)
        self._bitboards.queens = bb.BB_square(4) | bb.BB_square(60)
        self._bitboards.kings = bb.BB_square(5) | bb.BB_square(61)

    def __hash__(self) -> bb.Bitboards:
        return self._bitboards

    @property
    def is_over(self) -> bool:
        """True if 1 king left on board"""
        return sum(bb.reverse_scan_for_peice(self._bitboards.kings)) == 1

    @property
    def winner(self)-> bool | None:
        w:int = self._bitboards.white & self._bitboards.kings
        b:int = self._bitboards.black & self._bitboards.kings
        if w==b:
            return None
        elif w==0:
            return self.BLACK
        elif b==0:
            return self.WHITE

    @property
    def _occupied_squares(self) -> int:
        return self._bitboards.white | self._bitboards.black

    def _occupied_by_color(self, color:bool) -> int:
        return self._bitboards.white if color else self._bitboards.black

    @property
    def black_board(self) -> np.ndarray:
        return np.flip(self.board_to_numpy(), 0) * -1

    @property
    def white_board(self) -> np.ndarray:
        return self.board_to_numpy()

    @property
    def black_fog(self) -> np.ndarray:
        return np.flip(bb.bb_to_numpy(self._visable_squares(False)), 0)

    @property
    def white_fog(self) -> np.ndarray:
        return bb.bb_to_numpy(self._visable_squares(True))

    @property
    def white_foggy_board(self) -> np.ndarray:
        return self.apply_fog(self.white_board, self.white_fog)

    @property
    def black_foggy_board(self) -> np.ndarray:
        return self.apply_fog(self.black_board, self.black_fog)

    def apply_fog(self, board:np.ndarray, fog:np.ndarray) -> np.ndarray:
        return np.clip(board + np.logical_not(fog.copy())*20, -16, 15)  # This is a bit dumb but, I dunno


    def board_to_numpy(self) -> np.ndarray:
        return (
                bb.bb_to_numpy(self._bitboards.kings)*pce.Piece['K'].value
                + bb.bb_to_numpy(self._bitboards.queens)*pce.Piece['Q'].value
                + bb.bb_to_numpy(self._bitboards.pawns)*pce.Piece['P'].value
                + bb.bb_to_numpy(self._bitboards.rooks)*pce.Piece['R'].value
                + bb.bb_to_numpy(self._bitboards.bishops)*pce.Piece['B'].value
                + bb.bb_to_numpy(self._bitboards.knights)*pce.Piece['N'].value
               ) * (
                bb.bb_to_numpy(self._bitboards.black)*-1
                + bb.bb_to_numpy(self._bitboards.white)
        )

    def possible_moves(self)-> List[mv.Move]: pass #TODO: implement

    def make_move(self, Move)-> FOWChess: pass  #TODO: implement

    def make_random_move(self)-> FOWChess: pass  #TODO: implement

    def _visable_squares(self, color: bool)-> int:
        """
        Run through each piece type's move patterns to find all possible moves.
        """
        visable = 0

        our_pieces = self._occupied_by_color(color)
        visable |= our_pieces

        # Generate non-pawn moves.
        piece_moves = bb.reduce_with_bitwise_or(
            bb.attack_masks(frm, bb.piece_at(frm))
            for frm in (bb.reverse_scan_for_peice(our_pieces & ~self._bitboards.pawns))
        )
        visable |= piece_moves

        # If there are pawns, generate their moves
        pawns = self._bitboards.pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            pawn_attacks = bb.reduce_with_bitwise_or(
                    bb.pawn_attacks(frm, color) & self._occupied_by_color(not color)
                for frm in bb.reverse_scan_for_peice(pawns)
            )
            visable |= pawn_attacks

            # Then find their single and double moves
            if color == self.WHITE:
                single_moves = pawns << 8 & ~self._occupied_squares
                double_moves = (
                    single_moves << 8 & (bb.BB_rank(3) | bb.BB_rank(4)) & ~self._occupied_squares
                )
            else:
                single_moves = pawns >> 8 & ~self._occupied_squares
                double_moves = (
                    single_moves >> 8 & (bb.BB_rank(6) | bb.BB_rank(5)) & ~self._occupied_squares
                )
            visable |= single_moves | double_moves

            # Finally, check if an en passant is available
            if (self.board.ep_square and not
                bb.BB_square(self.board.ep_square) & self._occupied_squares):
                en_passant = self.board.ep_square #TODO: no idea how to do ep squares
                visable |= en_passant

        return visable
