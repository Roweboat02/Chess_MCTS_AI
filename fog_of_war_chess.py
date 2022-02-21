from __future__ import annotations

from typing import List

from random import choice as randchoice

import numpy as np

import bitboards as bb
import move as mv
import piece as pce


class FOWChess:
    WHITE = True
    BLACK = False

    def __init__(self, bitboards:bb.Bitboards, turn:bool) -> None:
        self.__current_turn: bool = turn # immutable
        self.__bitboards = bitboards # immutable
        self.__ep_square: bb.BB = bb.BB(0) # immutable #TODO

    @property
    def current_turn(self)->bool:
        return self.__current_turn

    @property
    def bitboards(self) -> bb.Bitboards:
        return self.__bitboards

    @property
    def ep_square(self) -> bb.BB:
        return self.__ep_square

    @classmethod
    def new_game(cls) -> FOWChess:
        return cls(bb.Bitboards.new_game(), cls.WHITE)

    def __hash__(self) -> bb.Bitboards:
        return self.bitboards # don't think so, but might need to encorporate turn

    @property
    def is_over(self) -> bool: # TODO: more termination checks
        """True if 1 king left on board"""
        return sum(bb.reverse_scan_for_piece(self.bitboards.kings)) == 1

    @property
    def winner(self) -> bool | None: # TODO: more termination checks
        w:int = self.bitboards.white & self.bitboards.kings
        b:int = self.bitboards.black & self.bitboards.kings
        if w==b:
            return None
        elif not w:
            return self.BLACK
        elif not b:
            return self.WHITE

    @property
    def _occupied_squares(self) -> int:
        return self.bitboards.white | self.bitboards.black

    def _occupied_by_color(self, color:bool) -> int:
        return self.bitboards.white if color else self.bitboards.black

    @property
    def black_board(self) -> np.ndarray:
        return np.flip(self.board_to_numpy(), 0) * -1

    @property
    def white_board(self) -> np.ndarray:
        return self.board_to_numpy()

    @property
    def black_fog(self) -> np.ndarray:
        return np.flip(self._visable_squares(False).bitboard_to_numpy(), 0)

    @property
    def white_fog(self) -> np.ndarray:
        return self._visable_squares(True).bitboard_to_numpy()

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
               self.bitboards.kings.bitboard_to_numpy() * pce.Piece['K'].value
               + self.bitboards.queens.bitboard_to_numpy() * pce.Piece['Q'].value
               + self.bitboards.pawns.bitboard_to_numpy() * pce.Piece['P'].value
               + self.bitboards.rooks.bitboard_to_numpy() * pce.Piece['R'].value
               + self.bitboards.bishops.bitboard_to_numpy() * pce.Piece['B'].value
               + self.bitboards.knights.bitboard_to_numpy() * pce.Piece['N'].value
               ) * (
               self.bitboards.black.bitboard_to_numpy() * -1
               + self.bitboards.white.bitboard_to_numpy()
        )

    def possible_moves(self) -> List[mv.Move]:
        moves:List[mv.Move] = []

        our_pieces:bb.BB = bb.BB(self._occupied_by_color(self.current_turn))
        their_pieces:bb.BB = bb.BB(self._occupied_by_color(not self.current_turn))
        pieces:bb.BB = our_pieces|their_pieces

        # Generate non-pawn moves.
        moves.extend([
                mv.Move(to, frm)
                        for frm in bb.reverse_scan_for_piece(our_pieces & ~self.bitboards.pawns)
                        for to in bb.reverse_scan_for_piece(mv.piece_move_mask(frm, self.bitboards.piece_at(frm), pieces) & ~our_pieces)
                ])

        # If there are pawns, generate their moves
        pawns = self.bitboards.pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            moves.extend( mv.Move(to, frm)
                for frm in bb.reverse_scan_for_piece(pawns)
                for to in bb.reverse_scan_for_piece(mv.pawn_attacks(frm, self.current_turn) & their_pieces)
            )

            # Then find their single and double moves
            if self.current_turn == self.WHITE:
                single_moves = (pawns << 8) & ~pieces
                double_moves = (single_moves << 8) & bb.BB.BB_rank(4) & ~pieces
            else:
                single_moves = pawns >> 8 & ~pieces
                double_moves = (single_moves >> 8) & bb.BB.BB_rank(6) & ~pieces

            moves.extend( mv.Move(to, to << 8) for to in bb.reverse_scan_for_piece(single_moves) )
            moves.extend( mv.Move(to, to << 16) for to in bb.reverse_scan_for_piece(double_moves) )

            if (self.ep_square and not
                bb.BB.BB_square(self.ep_square) & pieces):
                en_passant = self.ep_square #TODO: ep squares
                moves.extend([])

        return moves

    def make_move(self, move:mv.Move) -> FOWChess:
        return FOWChess(mv.make_move(self.bitboards, move), not self.current_turn)

    def make_random_move(self) -> FOWChess:
        return FOWChess(mv.make_move(self.bitboards, randchoice(self.possible_moves())), not self.current_turn)

    def _visable_squares(self, color: bool) -> bb.BB:
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
            mv.piece_move_mask(frm, self.bitboards.piece_at(frm), pieces) & ~our_pieces
            for frm in (bb.reverse_scan_for_piece(our_pieces & ~self.bitboards.pawns))
        )
        visable |= piece_moves

        # If there are pawns, generate their moves
        pawns = self.bitboards.pawns & our_pieces
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
                double_moves = single_moves << 8 & bb.BB.BB_rank(4) & ~pieces

            else:
                single_moves = pawns >> 8 & ~pieces
                double_moves = single_moves >> 8 & bb.BB.BB_rank(6) & ~pieces
            visable |= single_moves | double_moves

            # Finally, check if an en passant is available
            if (self.ep_square and not
                bb.BB.BB_square(self.ep_square) & pieces):
                en_passant = self.ep_square #TODO: ep squares
                visable |= en_passant

        return bb.BB(visable)
