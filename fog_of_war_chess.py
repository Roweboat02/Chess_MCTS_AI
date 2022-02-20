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
        a = cls(bb.Bitboards(bb.BB(0), bb.BB(0), bb.BB(0), bb.BB(0), bb.BB(0), bb.BB(0), bb.BB(0), bb.BB(0)))
        a._reset_board()
        return a

    def _reset_board(self) -> None:
        self._bitboards = self._bitboards.new_game()

    def __hash__(self) -> bb.Bitboards:
        return self._bitboards

    @property
    def is_over(self) -> bool:
        """True if 1 king left on board"""
        return sum(bb.reverse_scan_for_piece(self._bitboards.kings)) == 1

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
        return np.flip(bb.bitboard_to_numpy(self._visable_squares(False)), 0)

    @property
    def white_fog(self) -> np.ndarray:
        return bb.bitboard_to_numpy(self._visable_squares(True))

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
                       bb.bitboard_to_numpy(self._bitboards.kings) * pce.Piece['K'].value
                       + bb.bitboard_to_numpy(self._bitboards.queens) * pce.Piece['Q'].value
                       + bb.bitboard_to_numpy(self._bitboards.pawns) * pce.Piece['P'].value
                       + bb.bitboard_to_numpy(self._bitboards.rooks) * pce.Piece['R'].value
                       + bb.bitboard_to_numpy(self._bitboards.bishops) * pce.Piece['B'].value
                       + bb.bitboard_to_numpy(self._bitboards.knights) * pce.Piece['N'].value
               ) * (
                       bb.bitboard_to_numpy(self._bitboards.black) * -1
                       + bb.bitboard_to_numpy(self._bitboards.white)
        )

    def possible_moves(self)-> List[mv.Move]: pass #TODO: implement

    def make_move(self, Move)-> FOWChess: pass  #TODO: implement

    def make_random_move(self)-> FOWChess: pass  #TODO: implement

    def _visable_squares(self, color: bool)-> bb.BB:
        """
        Run through each piece type's move patterns to find all possible moves.
        """
        visable:bb.BB = bb.BB(0)

        our_pieces:bb.BB = bb.BB(self._occupied_by_color(color))
        their_pieces:bb.BB = bb.BB(self._occupied_by_color(not color))
        pieces:bb.BB = our_pieces|their_pieces

        visable |= our_pieces

        # Generate non-pawn moves.
        piece_moves = bb.reduce_with_bitwise_or(
            mv.piece_move_mask(frm, self._bitboards.piece_at(frm), pieces) & ~our_pieces
            for frm in (bb.reverse_scan_for_piece(our_pieces & ~self._bitboards.pawns))
        )
        visable |= piece_moves

        # If there are pawns, generate their moves
        pawns = self._bitboards.pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            pawn_attacks = bb.reduce_with_bitwise_or(
                    mv.pawn_attacks(frm, color) & their_pieces
                for frm in bb.reverse_scan_for_piece(pawns)
            )
            visable |= pawn_attacks

            # Then find their single and double moves
            if color == self.WHITE:
                single_moves = pawns << 8 & ~pieces
                double_moves = (
                    single_moves << 8 & (bb.BB.BB_rank(3) | bb.BB.BB_rank(4)) & ~pieces
                )
            else:
                single_moves = pawns >> 8 & ~pieces
                double_moves = (
                    single_moves >> 8 & (bb.BB.BB_rank(6) | bb.BB.BB_rank(5)) & ~pieces
                )
            visable |= single_moves | double_moves

            # Finally, check if an en passant is available
            if (self.board.ep_square and not
                bb.BB.BB_square(self.board.ep_square) & pieces):
                en_passant = self.board.ep_square #TODO: no idea how to do ep squares
                visable |= en_passant

        return bb.BB(visable)
