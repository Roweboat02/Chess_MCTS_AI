import random
from functools import reduce
import chess
import numpy as np


class Chess:
    mapped = {
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
    SQUARES_NEG_180 = [sq ^ 0x07 for sq in chess.SQUARES]

    def __init__(self, chess_game=None):
        self.board = chess.Board() if chess_game is None else chess_game
        self.calculate_from_chess()

    def calculate_from_chess(self) -> None:
        """
        Create numpy array representation of board and fog mask.

        """

        self.board_array = self.game_to_array()
        self.fog = self.generate_fog()
        self.moves = list(self.board.legal_moves)

    def test_color(self, color=None):
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

    def game_to_array(self, color=None):
        """
        Creates an 8x8 numpy array with each piece type represented by it's
        corresponding number in cls.mapped.
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
        color = self.test_color(color)

        # Given a chess.Piece, either return it's cls.mapped value or 0
        def piece_repr(piece):
            return self.mapped[piece.symbol()] if piece else 0

        # Iterate through all squares, convert to an (8x8) array repr
        # Unnecessary list comp for speed gains
        return np.reshape([piece_repr(self.board.piece_at(square))
                           for square in (chess.SQUARES_180
                                          if color else self.SQUARES_NEG_180)], (8, 8))

    def generate_fog(self, color=None):
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
        color = self.test_color(color)

        # Bitwise-or current position and possible moves
        # unnecessary list comp for speed gains (saves days of computation)
        mask = (self.board.occupied_co[color] | reduce(lambda x, y: x | y,
                                                       [chess.BB_SQUARES[sqr]
                                                        for sqr in self.possible_next_moves(color)]))

        # Mirror (for neural network consistency)
        mask ^= (0x38 if color else 0x07)

        # Convert the int64 (bit-board) mask to a 8x8 numpy mask array
        return np.resize(
                np.array(list(format(mask, 'b').zfill(64))) == '1',
                (8, 8))

    def possible_next_moves(self, turn):
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
        destinations = []
        add_to_dest = destinations.extend

        our_pieces = self.board.occupied_co[turn]
        their_pieces = self.board.occupied_co[not turn]
        pawn_attack_table = chess.BB_PAWN_ATTACKS[turn]  # specify the from location with [from_square]

        # Generate non-pawn moves.
        piece_moves = [sqr
                       for frm in (chess.scan_reversed(our_pieces & ~self.board.pawns))
                       for sqr in (chess.scan_reversed(self.board.attacks_mask(frm) & ~our_pieces))]
        add_to_dest(piece_moves)

        # If there are pawns, generate their moves
        pawns = self.board.pawns & our_pieces
        if pawns:
            # First if they can attack anyone
            pawn_attack = [sqr
                           for frm in chess.scan_reversed(pawns)
                           for sqr in (chess.scan_reversed(pawn_attack_table[frm] & their_pieces))]
            add_to_dest(pawn_attack)

            # Then find their single and double moves
            if turn == chess.WHITE:
                single_moves = pawns << 8 & ~self.board.occupied
                double_moves = single_moves << 8 & ~self.board.occupied & (chess.BB_RANK_3 | chess.BB_RANK_4)
            else:
                single_moves = pawns >> 8 & ~self.board.occupied
                double_moves = single_moves >> 8 & ~self.board.occupied & (chess.BB_RANK_6 | chess.BB_RANK_5)

            single_moves = [sqr for sqr in chess.scan_reversed(single_moves)]
            double_moves = [sqr for sqr in chess.scan_reversed(double_moves)]
            add_to_dest(single_moves)
            add_to_dest(double_moves)

            # Finally check if an en passant is available
            if self.board.ep_square and not chess.BB_SQUARES[self.board.ep_square] & self.board.occupied:
                en_passants = [self.board.ep_square]
                add_to_dest(en_passants)
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
        Wrapper for board.push('move')

        """
        self.board.push(move)

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
