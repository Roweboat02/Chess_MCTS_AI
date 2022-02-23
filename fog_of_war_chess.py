from __future__ import annotations

from typing import List, Tuple

from random import choice as rand_choice

import numpy as np

from bitboard_collections import Bitboard, ChessBitboards, SpecialMoveBitboards
from helper_functions import reverse_scan_for_piece, reduce_with_bitwise_or

import move as mv
from piece import Piece
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
        self.__special: SpecialMoveBitboards = special_moves  # Bitboards for castling/ep bitboards

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
        """Bitboards representing ep and castling bitboards"""
        return self.__special

    @classmethod
    def new_game(cls) -> FOWChess:
        """Alternate constructor for a FOWChess game, creates game in the standard chess board starting position."""
        return cls(ChessBitboards.new_game(), cls.WHITE, SpecialMoveBitboards.new_game())

    def make_move(self, move: mv.Move) -> FOWChess:
        """Given a move, create a FOWChess node where that move has been made."""
        return FOWChess(
                bitboards=self.bitboards.make_move(move),
                turn = not self.current_turn,
                special_moves=self.special_moves.update(self.bitboards, move))

    def make_random_move(self) -> FOWChess:
        """Make a randomly chosen move from the list of possible moves"""
        return self.make_move(rand_choice(self.possible_moves()))

    def __hash__(self) -> Tuple:
        return self.bitboards, self.__current_turn, self.__special

    @property
    def is_over(self) -> bool:  # TODO: better termination checks
        """True if 1 king left on board"""
        return sum(reverse_scan_for_piece(self.bitboards.kings)) == 1

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
                       self.bitboards.kings.bitboard_to_numpy() * Piece['K'].value
                       + self.bitboards.queens.bitboard_to_numpy() * Piece['Q'].value
                       + self.bitboards.pawns.bitboard_to_numpy() * Piece['P'].value
                       + self.bitboards.rooks.bitboard_to_numpy() * Piece['R'].value
                       + self.bitboards.bishops.bitboard_to_numpy() * Piece['B'].value
                       + self.bitboards.knights.bitboard_to_numpy() * Piece['N'].value
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
        everyones_pieces: Bitboard = our_pieces | their_pieces

        # Generate non-pawn moves.
        moves.extend([
            mv.Move(to=to, frm=frm)
            for frm in reverse_scan_for_piece(our_pieces & ~self.bitboards.pawns)
            for to in
            reverse_scan_for_piece(mv.piece_move_mask(frm, self.bitboards.piece_at(frm), everyones_pieces) & ~our_pieces)
        ])

        # TODO: Castling in Move
        # TODO: Mabye try and make castling checks it's own function.

        # check for castling
        if self.special_moves.castling_kings & our_pieces and self.special_moves.castling_rooks & our_pieces:
            backrank:Bitboard = Bitboard.from_rank(1) if self.current_turn else Bitboard.from_rank(8)
            a:Bitboard = backrank & Bitboard.from_file(1)
            b:Bitboard = backrank & Bitboard.from_file(2)
            c:Bitboard = backrank & Bitboard.from_file(3)
            d:Bitboard = backrank & Bitboard.from_file(4)

            f:Bitboard = backrank & Bitboard.from_file(6)
            g:Bitboard = backrank & Bitboard.from_file(7)
            h:Bitboard = backrank & Bitboard.from_file(8)

            our_king:Bitboard = self.bitboards.kings & our_pieces

            def anyone_attacking(square_mask:Bitboard) -> bool:
                """
                Using the principal of
                "Is one of their pieces attacking square" being logically the same as
                "If a piece of our color was on square, could it attack the same piece type of their color"
                determine if anyone is attacking square.
                """
                r_and_f_attackers = (self.bitboards.queens | self.bitboards.rooks) & their_pieces
                diag_attackers = (self.bitboards.queens | self.bitboards.bishops) & their_pieces
                king_attackers = (self.bitboards.kings | self.bitboards.queens) & their_pieces
                knight_attackers = self.bitboards.knights & their_pieces

                return any((
                        (self.bitboards.pawns & their_pieces) & mv.pawn_attacks(square_mask, self.current_turn),
                        (mv.rank_moves(square_mask, everyones_pieces) | mv.file_moves(square_mask, everyones_pieces)) & r_and_f_attackers,
                        mv.diagonal_moves(square_mask, everyones_pieces) & diag_attackers,
                        mv.king_moves(square_mask) & king_attackers,
                        mv.knight_moves(square_mask) & knight_attackers))


            # Try for kingside castle
            if (self.special_moves.castling_kings & our_pieces
                and self.special_moves.kingside_castling & our_pieces
                and ~everyones_pieces & (f | g)
                and not any(anyone_attacking(square) for square in (our_king, f, g))):
                    moves.append(mv.Move(to=g.bit_length(),
                                         frm=our_king.bit_length(),
                                         rook_to=f.bit_length(),
                                         rook_frm=h.bit_length()))
            # Try for queenside
            if (self.special_moves.castling_kings & our_pieces
                and self.special_moves.queenside_castling & our_pieces
                and ~everyones_pieces & (b | c | d)
                and not any(anyone_attacking(square) for square in (our_king, c, d))):
                    moves.append(mv.Move(to=c.bit_length(),
                                         frm=our_king.bit_length(),
                                         rook_frm=a.bit_length(),
                                         rook_to=d.bit_length()))

        # If there are pawns, generate their moves
        if pawns := self.bitboards.pawns & our_pieces:
            # First if they can attack anyone
            moves.extend(mv.Move(to, frm)
                         for frm in reverse_scan_for_piece(pawns)
                         for to in reverse_scan_for_piece(mv.pawn_attacks(frm, self.current_turn) & their_pieces)
                         )
            backrank:Bitboard
            # Then find their single and double moves
            if self.current_turn == self.WHITE:
                single_moves = (pawns << 8) & ~everyones_pieces
                double_moves = (single_moves << 8) & (Bitboard.from_rank(4) | Bitboard.from_rank(3)) & ~everyones_pieces
                backrank = Bitboard.from_rank(1)
            else:
                single_moves = pawns >> 8 & ~everyones_pieces
                double_moves = (single_moves >> 8) & (Bitboard.from_rank(6) | Bitboard.from_rank(5)) & ~everyones_pieces
                backrank = Bitboard.from_rank(8)

            moves.extend(mv.Move(to, to - 8) for to in reverse_scan_for_piece(single_moves))
            moves.extend(mv.Move(to, to - 16) for to in reverse_scan_for_piece(double_moves))

            # promotion
            if backrank & pawns:
                moves.extend(
                        (mv.Move(to=pawn.bit_length(),
                                frm=pawn.bit_length(),
                                promotion_to=Piece(promote * (-1 * (not self.current_turn))))
                         for pawn in reverse_scan_for_piece(pawns)
                         for promote in (2, 3, 4)))

            # Check for en passent
            if self.special_moves.ep_bitboard and not (self.special_moves.ep_bitboard & everyones_pieces):
                # "Is there one of our pawns attacking the ep square?"
                # is logically the same question as
                # "If there was one of their pawns on the ep square, would it be attacking one of our pawns?"
                ep_square:sq.Square = sq.Square(self.special_moves.ep_bitboard.bit_length())
                moves.extend([mv.Move(ep_square, sq.Square(frm.bit_length()))
                              for frm in reverse_scan_for_piece(
                                mv.pawn_attacks(ep_square, not self.current_turn) & pawns)])

        return moves

    def _visible_squares(self, color: bool) -> Bitboard:
        """
        Generate a bitboard of squares which should be visable to the param color (where True is white and black is False)
        """
        visible: Bitboard = Bitboard(0)

        our_pieces: Bitboard = Bitboard(self._occupied_by_color(color))
        their_pieces: Bitboard = Bitboard(self._occupied_by_color(not color))
        pieces: Bitboard = our_pieces | their_pieces

        visible |= our_pieces

        # Generate non-pawn moves.
        piece_moves = reduce_with_bitwise_or(
            mv.piece_move_mask(frm, self.bitboards.piece_at(frm), pieces) & ~our_pieces
            for frm in (reverse_scan_for_piece(our_pieces & ~self.bitboards.pawns))
        )
        visible |= piece_moves

        # If there are pawns, generate their moves
        if pawns := self.bitboards.pawns & our_pieces:
            # First if they can attack anyone
            pawn_attacks = reduce_with_bitwise_or(
                mv.pawn_attacks(frm, color) & their_pieces
                for frm in reverse_scan_for_piece(pawns)
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
            if self.special_moves.ep_bitboard and not (Bitboard.from_square(self.special_moves.ep_bitboard) & pieces):
                ep_square: sq.Square = sq.Square(self.special_moves.ep_bitboard.bit_length())
                visible |= reduce_with_bitwise_or( frm
                for frm in reverse_scan_for_piece(
                        mv.pawn_attacks(ep_square, not self.current_turn) & pawns))

        return Bitboard(visible)
