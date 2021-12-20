import random
from functools import reduce, cached_property
import chess
import numpy as np

def bitboard_to_numpy(bb):
    s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
    return np.unpackbits((bb >> s).astype(np.uint8), bitorder="little").reshape(8, 8)

class Chess:
    PIECE_ENCODING = {
        'P': 1,  # White Pawn
        'p': -1,  # Black Pawn
        'N': 2,  # White Knight
        'n': -2,  # Black Knight
        'B': 3,  # White Bishop
        'b': -3,  # Black Bishop
        'R': 4,  # White Rook
        'r': -4,  # Black Rook
        'Q': 5,  # White Queen
        'q': -5,  # Black Queen
        'K': 6,  # White King
        'k': -6  # Black King
    }

    _SQUARES_MIRRORED_LR = [sq ^ 0x07 for sq in chess.SQUARES]

    def __init__(self, chess_game=None):
        self.board = chess.Board() if chess_game is None else chess_game
        self.moves()
        self.game_array()
        self.fog()
        
    @cached_property
    def moves(self):
        return set(self.board.legal_moves)

    @cached_property
    def game_array(self, color=None):
        """
        Creates an 8x8 numpy array with each piece type represented by it's
        corresponding number in cls.PIECE_ENCODING.
        Note; arrays are oriented with the side who's turn it is down
        (like a chess board) and black sides are mirrored vertically
        such that a starting white and black board look the same.
        This is done for Neural network consistency.

        Parameters
        ----------
        color : bool, optional
            Which side to orient the array for. The default is None,
            which means to use the current turn instead.

        Returns
        -------
        numpy.ndarray
            (8,8) array representation of a chess board.

        """

        # If a colour isn't provided, use the current turn
        color = self.check_color(color)

        # Given a chess.Piece, either return it's cls.PIECE_ENCODING value or 0
        def piece_repr(piece):
            return self.PIECE_ENCODING[piece.symbol()] if piece else 0

        # Iterate through all squares, convert to an (8x8) array repr
        # Unnecessary list comp for speed gains
        return  np.reshape([piece_repr(self.board.piece_at(square))
            for square in (chess.SQUARES_180
                if color else self.SQUARES_MIRRORED_LR)], (8, 8))

    @cached_property
    def fog(self, color=None):
        """
        Creates a numpy mask representing the visible squares in a fog of war
        game of chess.
        Note; arrays are oriented with the side who's turn it is down
        (like a chess board) and black sides are mirrored vertically
        such that a starting white and black board look the same.
        This is done for Neural network consistency.

        Parameters
        ----------
        color : bool, optional
            Which side visibility is calculated for. The default is None.

        Returns
        -------
        numpy.ndarray
            (8,8) array mask representation of visibility of a chess board.

        """

        # If a colour isn't provided, use the current turn
        color = self.check_color(color)
        
        visable_squares = self.possible_destinations(color).union(self.possible_sources(color))

        # Bitwise-or current position and possible moves
        # unnecessary list comp for speed gains
        mask = reduce(lambda x, y: x | y,
                      (chess.BB_SQUARES[sqr] for sqr in visable_squares))

        # Mirror (for neural network consistency)
        # flip = (np.flipud if color else np.fliplr)

        # Convert the int64 (bit-board) mask to a 8x8 numpy mask array
        return bitboard_to_numpy(mask)

    def check_color(self, color=None):
        """
        Check if color is defined. If not use default value.
        Parameters
        Which side to orient the array for. The default is None,
        which means to use the current turn instead.

        """
        return color if bool(color) else self.board.turn

    @property
    def outcome(self):
        """
        Call outcome for board, game-state will be represented as
        WHITE, BLACK or 'tie.'

        Returns
        -------
        Win state. Either WHITE, BLACK or 'tie'

        """
        if not self.board.is_game_over():
            if (outcome := self.board.outcome().winner) is None:
                return 'tie'
            return outcome
        
    def _possible_sources(self, turn):
        return {sqr for sqr in chess.scan_reversed(self.board.occupied_co[turn])}

    def _possible_destinations(self, turn):
        """
        Run through each piece type's move patterns to find all possible moves.

        Parameters
        ----------
        turn : bool
            Who are the moves being generated for? chess.BLACK and chess.WHITE for example.

        Returns
        -------
        destinations : List
            DESCRIPTION.

        """
        destinations = set()

        our_pieces = self.board.occupied_co[turn]
        their_pieces = self.board.occupied_co[not turn]
        pawn_attack_table = chess.BB_PAWN_ATTACKS[turn]  # specify the from location with [from_square]

        # Generate non-pawn moves.
        piece_moves = {sqr
                       for frm in (chess.scan_reversed(our_pieces & ~self.board.pawns))
                       for sqr in (chess.scan_reversed(self.board.attacks_mask(frm) & ~our_pieces))}
        destinations = destinations.union(piece_moves)

        # If there are pawns, generate their moves
        pawns = self.board.pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            pawn_attack = {sqr
                           for frm in chess.scan_reversed(pawns)
                           for sqr in (chess.scan_reversed(pawn_attack_table[frm] & their_pieces))}
            destinations = destinations.union(pawn_attack)

            # Then find their single and double moves
            if turn == chess.WHITE:
                single_moves = pawns << 8 & ~self.board.occupied
                double_moves = single_moves << 8 & ~self.board.occupied & (chess.BB_RANK_3 | chess.BB_RANK_4)
            else:
                single_moves = pawns >> 8 & ~self.board.occupied
                double_moves = single_moves >> 8 & ~self.board.occupied & (chess.BB_RANK_6 | chess.BB_RANK_5)

            single_moves = {sqr for sqr in chess.scan_reversed(single_moves)}
            double_moves = {sqr for sqr in chess.scan_reversed(double_moves)}
            destinations = destinations.union(single_moves)
            destinations = destinations.union(double_moves)

            # Finally check if an en passant is available
            if self.board.ep_square and not chess.BB_SQUARES[self.board.ep_square] & self.board.occupied:
                en_passants = {self.board.ep_square}
                destinations = destinations.union(en_passants)
        return destinations

    def __repr__(self):
        """
        Simple conversion for printing.
        """
        chess.Board().__repr__()
        return np.array2string(self.board_array) + '\n' + str(self.board.turn) + '\n'

    def __str__(self):
        """
        Simple conversion for debugging.
        """
        return np.array2string(self.board_array)

    def has_winner(self):
        """
        Wrapper for chess 'is_game_over()'
        """
        return self.board.is_game_over()

    def make_move(self, move):
        """
        Wrapper for board.push('move') that clears cached attributes

        """
        self.board.push(move)
        self.clear_cache
        

    def make_random_move(self):
        """
        Make a random choice from available moves/

        """
        self.make_move(random.choice(self.moves))

    def make_questionable_move(self, move):
        """
        Function checks with "if move in self.moves", if for some reason you
        aren't sure if it's a legitimate move.

        """
        if move in self.moves:
            self.make_move(move)

    def copy(self):
        """
        Makes an identical copy of the chess game.

        """
        return Chess(self.board.copy())

    def reset(self):
        """
        Sets the board back to starting position and clears all cached info.

        """
        self.board.clear_board()
        self.clear_cache

    def clear_cache(self):
        del self.game_array, self.fog, self.moves
        


if __name__ == '__main__':
    print(Chess())