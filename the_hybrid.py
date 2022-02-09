import random
from functools import reduce, cached_property
import chess
import numpy as np


def bitboard_to_numpy(bb):
    s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
    return np.unpackbits((bb >> s).astype(np.uint8), bitorder="little").reshape(8, 8)


def reduce_with_bitwise_or(iterable):
    return reduce(lambda x, y: x | y, iterable)


class FOWChess:
    """
    Implements a fog of war (FOW) chess game.
    Intended to be used for machine learning.

    WHAT IS FOG OF WAR:
    FOW is a chess varient where each player can only see their pieces,
    and tiles those peices can legally move to.

    Checks and checkmates are absent in this varient, meaning any move can be
    made regardless of if the player's king is in check.

    The game only ends when a player's king is captured.

    (https://www.chess.com/terms/fog-of-war-chess)


    CONVENTIONS USED:
    This class uses a convention taken from the python chess library,
    where white is represented as True and black as False.

    """
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

    # _SQUARES_MIRRORED_LR = [sq ^ 0x07 for sq in chess.SQUARES]

    def __init__(self, chess_game=None, color=None):
        self.board = chess.Board() if chess_game is None else chess_game
        # self._color = color

    # def swap_color(self):
    #     self._color = not self._color
    #
    # @property
    # def color(self):
    #     return self._color if self._color is not None else self.board.turn

    @cached_property
    def moves(self):
        return list(self.board.pseudo_legal_moves)

    @cached_property
    def board_array(self):
        """
        Creates an 8x8 numpy arrays representing the current board, free of fog.

        Each piece type is represented by its corresponding number
        in cls.PIECE_ENCODING.

        Property is cached and only recalculated after a move has been made.
        """

        # Given a chess.Piece, either return it's cls.PIECE_ENCODING value or 0
        def piece_repr(piece):
            return self.DEFAULT_ENCODING[piece.symbol()] if piece else 0

        # Iterate through all squares, convert to an (8x8) array repr
        # Unnecessary list comp for speed gains
        board_array = np.reshape(
            [piece_repr(self.board.piece_at(square)) for square in chess.SQUARES_180],
                (8, 8))

        return np.dstack((np.flip(board_array, 0) * -1, board_array))

    @cached_property
    def fog(self):
        """
        Creates a numpy mask representing the visible squares in a fog of war
        game of chess.
        Note; arrays are oriented with the side whose turn it is down
        (like a chess board) and black sides are mirrored vertically
        such that a starting white and black board look the same.
        This is done for Neural network consistency.

        """
        # Convert the int64 (bit-board) mask to a 8x8 numpy mask array

        return np.dstack((
                np.flip(bitboard_to_numpy(self._visable_squares(False)), (0)),
                bitboard_to_numpy(self._visable_squares(True)),
                 ))

    @property
    def foggy_board(self):
        fog = np.logical_not(self.fog.copy())*100
        return np.clip(self.board_array + fog, -16, 15)

    @property
    def outcome(self):
        """
        Call outcome for board, game-state will be represented as
        WHITE, BLACK or 'tie.'

        Returns
        -------
        Win state. Either WHITE, BLACK or 'tie'

        """
        if self.board.is_game_over():
            if (outcome := self.board.outcome().winner) is None:
                return "tie"
            return outcome
        return None

    @property
    def finished(self):
        """
        Wrapper for chess 'is_game_over()'
        """
        return self.board.is_game_over()

    def __repr__(self):
        """
        Simple conversion for printing.
        """
        # chess.Board().__repr__()
        return f"""
            WHITE POV: \n {np.array2string(self.board_array[:,:,1])} \n  
            BLACK POV: \n {np.array2string(self.board_array[:,:,0])} \n
            Current turn: {self.board.turn}
            """

    def __str__(self):
        """
        Simple conversion for debugging.
        """
        return self.__repr__()

    def make_move(self, move):
        """
        Makes a chess.Move.
        NOTE: doesn't check if a move is valid.

        Clears cached properties

        """
        self.board.push(move)
        self.clear_cache()

    def make_random_move(self):
        """
        Make a random choice from available moves

        Clears cached properties
        """
        self.make_move(random.choice(self.moves))

    def make_and_check_move(self, move):
        """
        Function checks with "if move in self.moves", if for some reason you
        aren't sure if a legitimate move.

        Clears cached properties
        """
        if move in self.moves:
            self.make_move(move)

    def copy(self):
        """
        Makes an identical copy of the chess game.

        """
        return FOWChess(self.board.copy())

    def reset(self):
        """
        Sets the board back to starting position and clears all cached info.

        """
        self.board.clear_board()
        self.clear_cache()

    def clear_cache(self):
        for attr in ("fog", "moves", "board_array"):
            self.__dict__.pop(attr, None)

    # def piece_encoding(self):
    #     if self._color is None:
    #         color = True
    #     else:
    #         color = self._color
    #
    #     return {k: v * (-1 if not color else 1) for k, v in self.DEFAULT_ENCODING.items()}

    def _visable_squares(self, color):
        """
        Run through each piece type's move patterns to find all possible moves.

        Returns
        -------
        destinations : List
            DESCRIPTION.

        """
        visable = 0

        our_pieces = self.board.occupied_co[color]
        visable |= our_pieces

        # Generate non-pawn moves.
        piece_moves = reduce_with_bitwise_or(
            self.board.attacks_mask(frm)
            for frm in (chess.scan_reversed(our_pieces & ~self.board.pawns))
        )
        visable |= piece_moves

        # If there are pawns, generate their moves
        pawns = self.board.pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            pawn_attacks = reduce_with_bitwise_or(
                chess.BB_PAWN_ATTACKS[color][frm] & self.board.occupied_co[not color]
                for frm in chess.scan_reversed(pawns)
            )
            visable |= pawn_attacks

            # Then find their single and double moves
            if color == chess.WHITE:
                single_moves = pawns << 8 & ~self.board.occupied
                double_moves = (
                    single_moves << 8 & (chess.BB_RANK_3 | chess.BB_RANK_4) & ~self.board.occupied
                )
            else:
                single_moves = pawns >> 8 & ~self.board.occupied
                double_moves = (
                    single_moves >> 8 & (chess.BB_RANK_6 | chess.BB_RANK_5) & ~self.board.occupied
                )
            visable |= single_moves | double_moves

            # Finally, check if an en passant is available
            if (self.board.ep_square and not
                chess.BB_SQUARES[self.board.ep_square] & self.board.occupied):
                en_passant = self.board.ep_square
                visable |= en_passant

        return visable



if __name__ == "__main__":
    a = FOWChess()
    print(a)
    print(a.board)
    for _ in range (40):
        a.make_random_move()
    print(a.board)
    print(a)
    print("w")
    b = a.foggy_board
    print(b[:,:,1])
    print("b")
    print(b[:,:,0])
