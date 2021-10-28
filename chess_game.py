# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 14:01:05 2021

@author: noahr

Monte carlo tree search class and functions.
A game needs to have:
    Class attributes:
    SYMBOLS : iterable
        SYMBOLS Should include all differentiations between players.
        Is never used stricly as a class attribute, but must be constant.

    Object attributes:
    turn : obj from SYMBOLS (i.e. int, str, ect.)
        an object belonging to SYMBOLS which is used to denote which player
        is expected to make an action.
    winner : obj from SYMBOLS (i.e. int, str, ect.)
        an object belonging to SYMBOLS which is used to denote which player
        has won. Winner should be updated by game class after a state change.
    Methods:
    next_moves_list()
        Returns a list or array of all reachable states immediately after the
            current game state.
    copy()
        Returns an identical, entirely independant copy of the game in it's
        current state.
    make_move(move)
        Change from current game state to state described with move param.
    make_random_move()
        Change from current game state to an immediately reachable randomly
        selected state.
"""

import random
from functools import reduce
import chess
import numpy as np


class Chess:


    mapped = {
        'P': 1,     # White Pawn
        'p': -1,    # Black Pawn
        'N': 2,     # White Knight
        'n': -2,    # Black Knight
        'B': 3,     # White Bishop
        'b': -3,    # Black Bishop
        'R': 4,     # White Rook
        'r': -4,    # Black Rook
        'Q': 5,     # White Queen
        'q': -5,    # Black Queen
        'K': 6,     # White King
        'k': -6     # Black King
    }
    SQUARES_NEG_180 = [sq ^ 0x07 for sq in chess.SQUARES]

    def __init__(self, chess_game=None):
        self.board = chess.Board() if chess_game is None else chess_game
        self.calculate_from_chess()

    def calculate_from_chess(self):
        """
        Create numpy array representation of board and fog mask.

        """

        self.board_array = self.game_to_array()
        self.fog = self.generate_fog()
        self.moves = list(self.board.legal_moves)

    @property
    def outcome(self):
        """
        Call outcome() for board, convert to WHITE, BLACK or 'tie'

        Returns
        -------
        Win state. Either WHITE, BLACK or 'tie'

        """
        if not self.board.is_game_over():

            if (out := self.board.outcome().winner) is None:
                return 'tie'
            return out

    def game_to_array(self, color=None):
        """
        Creates an 8x8 numpy array with each piece type represented by it's
        corrisponding number in cls.mapped.
        Note; arrays are oriented with the side who's turn it is down
        (like a chess board) and black sides are mirrored vertically
        such that a starting white and black board look the same.
        This is done for Neural network consistency.

        Parameters
        ----------
        color : bool, optional
            Which side to orient the array for. The default is None.

        Returns
        -------
        numpy.ndarray
            (8,8) array representation of a chess board.

        """

        # If a colour isn't provided, use the current turn
        color = color if bool(color) else self.board.turn

        # Given a chess.Piece, either return it's cls.mapped value or 0
        piece_repr = lambda piece : self.mapped[piece.symbol()] if piece else 0

        # Iterate through all squares, convert to an (8x8) array repr
        # Unessiccary list comp for speed gains (saves days of computation)
        return np.reshape(
            [piece_repr(self.board.piece_at(square))
             for square in (chess.SQUARES_180 if color
                            else self.SQUARES_NEG_180)], (8,8))

    def generate_fog(self, color=None):
        """
        Creates a numpy mask representing the visable squares in a fog of war
        game of chess.
        Note; arrays are oriented with the side who's turn it is down
        (like a chess board) and black sides are mirrored vertically
        such that a starting white and black board look the same.
        This is done for Neural network consistency.

        Parameters
        ----------
        color : bool, optional
            Which side visability is calculated for. The default is None.

        Returns
        -------
        numpy.ndarray
            (8,8) array mask representation of visability of a chess board.

        """

        # If a colour isn't provided, use the current turn
        color = color if color else self.board.turn

        # Bitwise-or current position and possible moves
        # Unessiccary list comp for speed gains (saves days of computation)
        mask = (self.board.occupied_co[color] | reduce(lambda x,y : x|y,
                         [chess.BB_SQUARES[sqr]
                          for sqr in self.possible_destinations(self.board,
                                                                color)]))

        # Mirror (for neural network consistancy)
        mask ^= (0x38 if color else 0x07)

        # Convert the int64 (bit-board) mask to a 8x8 numpy mask array
        return np.resize(
            np.array(list(format(mask, 'b').zfill(64))) == '1',
            (8,8))

    def possible_destinations(self, turn):
        """


        Parameters
        ----------
        turn : TYPE
            DESCRIPTION.

        Returns
        -------
        destinations : TYPE
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

        # If there are pawns, generate thier moves
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


        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        chess.Board().__repr__()
        return np.array2string(self.board_array) + '\n' + self.board.turn + '\n'

    def __str__(self):
        """


        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return np.array2string(self.board_array)

    def has_winner(self):
        """


        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.board.is_game_over()

    def make_move(self, move):
        """


        Parameters
        ----------
        move : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.board.push(move)

    def make_random_move(self):
        """


        Returns
        -------
        None.

        """
        self.make_move(random.choice(self.moves))

    def make_questionable_move(self, move):
        """


        Parameters
        ----------
        move : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if move in self.moves:
            self.make_move(move)

    def copy(self):
        """


        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return Chess(self.board.copy())

    def reset(self):
        """


        Returns
        -------
        None.

        """
        self.board.clear_board()
