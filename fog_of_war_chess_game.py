import random
from functools import reduce, cached_property
import chess
import numpy as np
import copy

def bitboard_to_numpy(bb):
    """Translates an interger to a 8x8 numpy array of it's bits"""
    s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
    return np.unpackbits((bb >> s).astype(np.uint8), bitorder="little").reshape(8, 8)


def reduce_with_bitwise_or(iterable):
    """Bitwise-or items in an iterable container together until one is left."""
    return reduce(lambda x, y: x | y, iterable)


def apply_fog(boards, fogs):
    """
    Apply fog arrays to board arrays where -10 is a foggy tile.

    Takes two iterables (ordered black, white) of np.arrays.
    The first iterable should be board representations.
    The second iterable should be boolean arrays, where "True" tiles are visable.

    Returns
    list: ordered (black, white) of each side's board, with it's fog applied.
    """
    return [board.copy()[np.logical_not(fog)] = -10 for board in boards]


class FogOfWarChess:
    """
    Implements a fog of war (FOW) chess game.
    Intended to be used for machine learning.

    WHAT IS FOG OF WAR:
    FOW is a chess varient where each player can only see their pieces,
    and and tiles those peices can legally move to.

    Checks and checkmates are absent in this varient, meaning any move can be
    made regardless of if the player's king is in check.

    The game only ends when a player's king is captured.

    (https://www.chess.com/terms/fog-of-war-chess)


    CONVENTIONS USED:
    This class uses a convention taken from the python chess library,
    where white is represented as True and black as False.

    """

    # Numerical encoding for chess pieces
    PIECE_ENCODING = {
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

    def __init__(self, chess_game=None):
        """
        Create a FOW game in the standard chess starting position,
        unless an existing chess.Board is provided.
        """
        self.board = chess.Board() if chess_game is None else chess_game

    @property
    def turn(self):
        """Return a bool for which color's turn it is."""
        return self.board.turn

    @cached_property
    def moves(self):
        """
        Generate a list of legal moves the current player can make.

        Property is cached and only recalculated after a move has been made.
        """  
        return list(self.board.pseudo_legal_moves)
        # Has to be a list and not a set for random choice to work. Dumb.

    @cached_property
    def board_array(self):
        """
        Creates an 8x8 numpy arrays representing the current board, free of fog.
         
        Each piece type is represented by it's corresponding number
        in cls.PIECE_ENCODING.

        Property is cached and only recalculated after a move has been made.
        """

        # Given a chess.Piece, either return it's cls.PIECE_ENCODING value or 0
        def piece_repr(piece):
            return self.piece_encoding[piece.symbol()] if piece else 0

        # Iterate through all squares, convert to an (8x8) array repr
        # Unnecessary list comp for speed gains
        board_array = np.reshape(
            [piece_repr(self.board.piece_at(square)) 
            for square in chess.SQUARES_180],
            (8, 8))

        return board_array

    @cached_property
    def fog(self):
        """
        Creates two bool np.arrays of tiles visable from both player's POV's.

        Returns a tuple ordered black then white so using 0 or False as an index
        accsesses black's items and 1 or True for white.
        
        Property is cached and only recalculated after a move has been made.
        """

        # Convert the int64 (bit-board) mask to a 8x8 numpy mask array
        return (bitboard_to_numpy(self._visable_squares(False)),
            bitboard_to_numpy(self._visable_squares(True)))

    @property
    def outcome(self):
        """
        Outcome of the game, represented as WHITE, BLACK, 'tie' or None if ongoing.
        """
        if self.board.is_game_over():
            if (outcome := self.board.outcome().winner) is None:
                return "tie"
            return outcome
        return None

    @property
    def finished(self):
        """
        Boolean for if the game is over (True), or not (False).
        """
        return self.board.is_game_over()

    def __repr__(self):
        """
        Simple conversion for printing.
        """
        chess.Board().__repr__()
        return np.array2string(self.board_array) + "\n"
         + str('white' if self.board.turn else 'black') + "\n"

    def __str__(self):
        """
        Simple conversion for debugging.
        """
        return np.array2string(self.board_array)

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
        Copies and returns self. 

        """
        return copy.deepcopy(self)

    def reset(self):
        """
        Sets the board back to starting position.

        Clears cached properties
        """
        self.board.clear_board()
        self.clear_cache()

    def clear_cache(self):
        """
        Function which deletes variables named,
        "fog", "moves" and "board_array" if they're defined.
        """
        for attr in ("fog", "moves", "board_array"):
            self.__dict__.pop(attr, None)

    def _visable_squares(self, color):
        """
        Find all legal origin and destination tiles. 

        This is done by bitwise-or-ing a bunch of the chess.Board's bitboards together.

        Returns a int, which if interpretted as a 64 bit, 0-pre-appended interger,
        each bit corresponds to a chess tile.
        If the bit is a 0, the tile is covered with fog.
        If the bit is a 1, the tile is visable.
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

            # Finally check if an en passant is available
            if (self.board.ep_square and not
                chess.BB_SQUARES[self.board.ep_square] & self.board.occupied):
                en_passant = self.board.ep_square
                visable |= en_passant

        return visable


if __name__ == "__main__":

