from collections.abc import Iterator, Iterable
from functools import reduce

import numpy as np

def reduce_with_bitwise_or(iterable:Iterable[int]) -> int:
    return reduce(lambda x, y: x | y, iterable)

def BB_rank(num:int) -> int:
    return 0b11111111 << (num-1)*8

def BB_file(num:int) -> int:
    return 0x0101_0101_0101_0101 << (num-1)*8

def BB_square(num:int) -> int:
    return 1<<(num-1)

def reverse_scan_for_peice(bitboard:int) -> Iterator[int]:
    while bitboard:
        length = bitboard.bit_length()-1
        yield length
        bitboard ^= 1<<length


class FOWChess:
    WHITE = True
    BLACK = False

    DEFAULT_ENCODING = {
        "P": 1,  # White Pawn
        "p": -1,  # Black Pawn
        "N": 2,  # White Knight
        "n": -2,  # Black Knight
        "B": 3,  # White Bishop
        "b": -3,  # Black Bishop
        "R": 4,  # White Rook
        "r": -4,  # Black Rook
        "Q": 5,  # White Queen
        "q": -5,  # Black Queen
        "K": 6,  # White King
        "k": -6,  # Black King
    }

    def __init__(self):
        self._white = 0
        self._black = 0
        self._pawns = 0
        self._knights = 0
        self._bishops = 0
        self._rooks = 0
        self._queens = 0
        self._kings = 0
        self.reset_board()

    def reset_board(self) -> None:
        self._white = BB_rank(1)|BB_rank(2)
        self._black = BB_rank(7)|BB_rank(8)
        self._pawns = BB_rank(7)|BB_rank(2)
        self._bishops = BB_square(3)|BB_square(6)|BB_square(58)|BB_square(62)
        self._knights = BB_square(2)|BB_square(7)|BB_square(57)|BB_square(63)
        self._rook = BB_square(1)|BB_square(8)|BB_square(56)|BB_square(64)
        self._queens = BB_square(4)|BB_square(60)
        self._kings = BB_square(5)|BB_square(61)

    def __hash__(self):
        return (self._white,
                self._black,
                self._pawns,
                self._knights,
                self._bishops,
                self._rooks,
                self._queens,
                self._kings,
                )

    @property
    def occupied_squares(self) -> int:
        return self._white & self._black

    def occupied_by_color(self, color:bool) -> int:
        return self._white if color else self._black

    @property
    def black_fog(self) -> np.ndarray:
        return np.flip(self.bb_to_numpy(self._visable_squares(False)), 0)

    @property
    def white_fog(self) -> np.ndarray:
        return self.bb_to_numpy(self._visable_squares(True))

    def make_move(self, move): pass

    def _remove_peice_at(self, square, peice): pass

    def _put_piece_at(self, square, peice): pass

    def board_to_numpy(self) -> np.ndarray:
        return (
                self.bb_to_numpy(self._kings)*self.DEFAULT_ENCODING['K']
                + self.bb_to_numpy(self._queens)*self.DEFAULT_ENCODING['Q']
                + self.bb_to_numpy(self._pawns)*self.DEFAULT_ENCODING['P']
                + self.bb_to_numpy(self._rooks)*self.DEFAULT_ENCODING['R']
                + self.bb_to_numpy(self._bishops)*self.DEFAULT_ENCODING['B']
                + self.bb_to_numpy(self._knights)*self.DEFAULT_ENCODING['K']
               ) * (
                self.bb_to_numpy(self._black)*-1
                + self.bb_to_numpy(self._white)
        )


    def bb_to_numpy(self, bb: int) -> np.ndarray:
        return np.unpackbits((bb>>np.arange(0, 57, 8)).astype(np.uint8), bitorder="little").reshape(8, 8)

    def possible_moves(self): pass

    def _visable_squares(self, color: bool) -> int:
        """
        Run through each piece type's move patterns to find all possible moves.

        Returns
        -------
        destinations : List
            DESCRIPTION.

        """
        visable = 0

        our_pieces = self.occupied_by_color(color)
        visable |= our_pieces

        # Generate non-pawn moves.
        piece_moves = reduce_with_bitwise_or(
            self.board.attacks_mask(frm)
            for frm in (reverse_scan_for_peice(our_pieces & ~self._pawns))
        )
        visable |= piece_moves

        # If there are pawns, generate their moves
        pawns = self._pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            pawn_attacks = reduce_with_bitwise_or(
                chess.BB_PAWN_ATTACKS[color][frm] & self.occupied_by_color(not color)
                for frm in reverse_scan_for_peice(pawns)
            )
            visable |= pawn_attacks

            # Then find their single and double moves
            if color == self.WHITE:
                single_moves = pawns << 8 & ~self.occupied_squares
                double_moves = (
                    single_moves << 8 & (BB_rank(3) | BB_rank(4)) & ~self.occupied_squares
                )
            else:
                single_moves = pawns >> 8 & ~self.occupied_squares
                double_moves = (
                    single_moves >> 8 & (BB_rank(6) | BB_rank(5)) & ~self.occupied_squares
                )
            visable |= single_moves | double_moves

            # Finally, check if an en passant is available
            if (self.board.ep_square and not
                BB_square(self.board.ep_square) & self.occupied_squares):
                en_passant = self.board.ep_square
                visable |= en_passant

        return visable
