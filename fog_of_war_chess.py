from __future__ import annotations

from typing import List, Tuple

from random import choice as rand_choice

import numpy as np

from bitboards import Bitboard, ChessBitboards, SpecialMoveBitboards
import bitboards as bb

import move as mv
import piece as pce
import square as sq


def apply_fog(board: np.ndarray, fog: np.ndarray) -> np.ndarray:
    """
    Apply fog to board
    @param board: 8x8 numpy array representing a chess board
    @param fog:  8x8 numpy array representing fog over a chess board
    @return foggy_board: 8x8 numpy array representing a chess board with fog applied. Fog is represented as 15.
    """
    return np.clip(board + np.logical_not(fog.copy()) * 20, -16, 15)  # This is a bit dumb, but I dunno


class FOWChess:
    WHITE = True
    BLACK = False

    def __init__(self, bitboards: ChessBitboards, turn: bool, special_moves: SpecialMoveBitboards) -> None:
        # immutable
        self.__current_turn: bool = turn  # color of the current player
        self.__bitboards = bitboards  # Interger bitboards of both colors and all pieces
        self.__special: SpecialMoveBitboards = special_moves  # Bitboards for castling/ep rights

    @property
    def current_turn(self) -> bool:
        """Color of the current player. True if white, False if black"""
        return self.__current_turn

    @property
    def bitboards(self) -> ChessBitboards:
        """Bitboards representing pieces and colors"""
        return self.__bitboards

    @property
    def special_moves(self) -> SpecialMoveBitboards:
        """Bitboards representing ep squares and casling rights"""
        return self.__special

    @classmethod
    def new_game(cls) -> FOWChess:
        """Alternate constructor for a FOWChess game, in the standard chess board starting position."""
        return cls(ChessBitboards.new_game(), cls.WHITE, SpecialMoveBitboards.new_game())

    @property
    def castling_rights(self) -> Bitboard:
        """The kings and rooks of current turn's player, who can still legally castle"""
        return self.__special.castling_rights(self.__bitboards.white if self.__current_turn else self.__bitboards.black)

    def make_move(self, move: mv.Move) -> FOWChess:
        """
        Given a move, create a set of bitboards with that move made.
        Checking if move is valid is responsibility of caller.
        """
        return FOWChess(
                bitboards=self.bitboards.make_move(move),
                turn = not self.current_turn,
                special_moves=self.special_moves.update(self.bitboards, move))

    def make_random_move(self) -> FOWChess:
        return self.make_move(rand_choice(self.possible_moves()))

    def __hash__(self) -> Tuple:
        return self.bitboards, self.__current_turn, self.__special

    @property
    def is_over(self) -> bool:  # TODO: better termination checks
        """True if 1 king left on board"""
        return sum(bb.reverse_scan_for_piece(self.bitboards.kings)) == 1

    @property
    def winner(self) -> bool | None:  # mabye make this a class
        """Return True if white, False if Black, None if not over."""
        w: int = self.bitboards.white & self.bitboards.kings
        b: int = self.bitboards.black & self.bitboards.kings
        if w == b:
            return None
        elif not w:
            return self.BLACK
        elif not b:
            return self.WHITE

    @property
    def board_as_numpy(self) -> np.ndarray:
        """A numpy representation of the chess board, using intergers. See Piece enum for encoding"""
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

    @property
    def black_board(self) -> np.ndarray:
        """Numpy array representation of board, with black on the bottom."""
        return np.flip(self.board_as_numpy, 0) # * -1 and mirror about 1 as erll if you want it to look like white

    @property
    def white_board(self) -> np.ndarray:
        """Numpy array representation of board, where white is on bottom"""
        return self.board_as_numpy

    @property
    def black_fog(self) -> np.ndarray:
        """Numpy array representation of black's fog, where black is on bottom"""
        return np.flip(self._visible_squares(False).bitboard_to_numpy(), 0)

    @property
    def white_fog(self) -> np.ndarray:
        """Numpy array representation of white's fog, where white is on bottom"""
        return self._visible_squares(True).bitboard_to_numpy()

    @property
    def white_foggy_board(self) -> np.ndarray:
        """Numpy array representation of board with white's fog applied, where white is on bottom"""
        return apply_fog(self.white_board, self.white_fog)

    @property
    def black_foggy_board(self) -> np.ndarray:
        """Numpy array representation of board with black's fog applied, where black is on bottom"""
        return apply_fog(self.black_board, self.black_fog)

    def _occupied_by_color(self, color: bool) -> Bitboard:
        """White's bitboard if True, black's if False"""
        return self.bitboards.white if color else self.bitboards.black

    def possible_moves(self) -> List[mv.Move]:
        """List of possible moves the current player can legally make."""
        moves: List[mv.Move] = []

        our_pieces: Bitboard = self._occupied_by_color(self.current_turn)
        their_pieces: Bitboard = self._occupied_by_color(not self.current_turn)
        pieces: Bitboard = our_pieces | their_pieces

        # Generate non-pawn moves.
        moves.extend([
            mv.Move(to, frm)
            for frm in bb.reverse_scan_for_piece(our_pieces & ~self.bitboards.pawns)
            for to in
            bb.reverse_scan_for_piece(mv.piece_move_mask(frm, self.bitboards.piece_at(frm), pieces) & ~our_pieces)
        ])

        # TODO: Castling in moves
        # TODO: Theres def a simpler way than double ifs but I'm lazy atm

        # Try for castling
        # BTW the chess rule book said only the two squares the king covers matters.

        # White castling
        if self.current_turn:
            # Try for kingside castle
            if self.castling_rights & ~(Bitboard.from_square(sq.Square(6)) & Bitboard.from_square(sq.Square(7))):
                moves.append(mv.Move(sq.Square(5), mv.Square(7)))
            # Try for queenside
            if self.castling_rights & ~(Bitboard.from_square(sq.Square(4)) & Bitboard.from_square(sq.Square(3))):
                moves.append(mv.Move(sq.Square(1), mv.Square(4)))
        # Black castling
        else:
            # Try for kingside castle
            if self.castling_rights & ~(Bitboard.from_square(sq.Square(62)) & Bitboard.from_square(sq.Square(63))):
                moves.append(mv.Move(sq.Square(61), mv.Square(64)))
            # Try for queenside
            if self.castling_rights & ~(Bitboard.from_square(sq.Square(59)) & Bitboard.from_square(sq.Square(60))):
                moves.append(mv.Move(sq.Square(61), mv.Square(57)))

        # If there are pawns, generate their moves
        pawns = self.bitboards.pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            moves.extend(mv.Move(to, frm)
                         for frm in bb.reverse_scan_for_piece(pawns)
                         for to in bb.reverse_scan_for_piece(mv.pawn_attacks(frm, self.current_turn) & their_pieces)
                         )

            # Then find their single and double moves
            if self.current_turn == self.WHITE:
                single_moves = (pawns << 8) & ~pieces
                double_moves = (single_moves << 8) & Bitboard.from_rank(4) & ~pieces
            else:
                single_moves = pawns >> 8 & ~pieces
                double_moves = (single_moves >> 8) & Bitboard.from_rank(6) & ~pieces

            moves.extend(mv.Move(to, to << 8) for to in bb.reverse_scan_for_piece(single_moves))
            moves.extend(mv.Move(to, to << 16) for to in bb.reverse_scan_for_piece(double_moves))

            if self.special_moves.ep_square and not (Bitboard.from_square(self.special_moves.ep_square) & pieces):
                moves.extend([mv.Move(to, sq.Square(self.special_moves.ep_square))
                              for pawn in bb.reverse_scan_for_piece(pawns)
                              for to in bb.reverse_scan_for_piece(mv.pawn_attacks(pawn, self.current_turn) & their_pieces)
                              if self.special_moves.ep_square & to])

        return moves

    def _visible_squares(self, color: bool) -> Bitboard:
        """
        Generate a bitboard of squares which should be visable to the param color (where True is white and black is false)
        """
        visible: Bitboard = Bitboard(0)

        our_pieces: Bitboard = Bitboard(self._occupied_by_color(color))
        their_pieces: Bitboard = Bitboard(self._occupied_by_color(not color))
        pieces: Bitboard = our_pieces | their_pieces

        visible |= our_pieces

        # Generate non-pawn moves.
        piece_moves = bb.reduce_with_bitwise_or(
            mv.piece_move_mask(frm, self.bitboards.piece_at(frm), pieces) & ~our_pieces
            for frm in (bb.reverse_scan_for_piece(our_pieces & ~self.bitboards.pawns))
        )
        visible |= piece_moves

        # If there are pawns, generate their moves
        pawns = self.bitboards.pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            pawn_attacks = bb.reduce_with_bitwise_or(
                mv.pawn_attacks(frm, color) & their_pieces
                for frm in bb.reverse_scan_for_piece(pawns)
            )
            visible |= pawn_attacks

            # Then find their single and double moves
            if color == self.WHITE:
                single_moves = pawns << 8 & ~pieces
                double_moves = single_moves << 8 & Bitboard.from_rank(4) & ~pieces

            else:
                single_moves = pawns >> 8 & ~pieces
                double_moves = single_moves >> 8 & Bitboard.from_rank(6) & ~pieces
            visible |= single_moves | double_moves

            # Finally, check if an en passant is available
            if self.special_moves.ep_square and not (Bitboard.from_square(self.special_moves.ep_square) & pieces):
                visible |= bb.reduce_with_bitwise_or(
                    sq.Square(self.special_moves.ep_square) for pawn in bb.reverse_scan_for_piece(pawns)
                    for to in bb.reverse_scan_for_piece(mv.pawn_attacks(pawn, self.current_turn) & their_pieces)
                    if self.special_moves.ep_square & to)

        return Bitboard(visible)
