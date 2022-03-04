"""
test_fog_of_war.py
Test functionality of the FOWChess class.

Author: Noah Rowe
Date: 2022/02/24
Last Modified: 2022/02/25
    Finishing the last of the unit tests
"""
from typing import Set
from unittest import TestCase

import numpy as np

from fog_of_war.chess_bitboards import ChessBitboards
from fog_of_war.special_move_bitboards import SpecialMoveBitboards
from fog_of_war.fog_of_war_chess import FOWChess
from fog_of_war.bitboard import Bitboard
from fog_of_war.square import Square
from fog_of_war.move import Move


class TestFOWChess(TestCase):
    """Test suite for FOWChess functionality"""
    def setUp(self):
        """Set up before each test"""
        self.new_game_by_hand: FOWChess = FOWChess(
            bitboards=ChessBitboards.new_game(),
            turn=True,
            special_moves=SpecialMoveBitboards.new_game(),
            half_move=0
        )

        self.new_game_numpy = np.array(
            [[-4, -2, -3, -5, -6, -3, -2, -4],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [4, 2, 3, 5, 6, 3, 2, 4]])

        self.white_move = Move(to=Square.e4, frm=Square.e2)

        self.white_move_numpy = np.array(
            [[-4, -2, -3, -5, -6, -3, -2, -4],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 0, 1, 1, 1],
             [4, 2, 3, 5, 6, 3, 2, 4]])

        self.white_move_board_by_hand: FOWChess = FOWChess(
            bitboards=ChessBitboards(
                white=((Bitboard.from_rank(1) | Bitboard.from_rank(2))
                       & ~Bitboard.from_square(Square.e2)
                       | Bitboard.from_square(Square.e4)),

                black=Bitboard.from_rank(7) | Bitboard.from_rank(8),

                pawns=(Bitboard.from_rank(7) | Bitboard.from_rank(2)
                       & ~Bitboard.from_square(Square.e2)
                       | Bitboard.from_square(Square.e4)),

                knights=(Bitboard.from_square(Square.b1)
                         | Bitboard.from_square(Square.g1)
                         | Bitboard.from_square(Square.b8)
                         | Bitboard.from_square(Square.g8)),

                bishops=(Bitboard.from_square(Square.c1)
                         | Bitboard.from_square(Square.f1)
                         | Bitboard.from_square(Square.c8)
                         | Bitboard.from_square(Square.f8)),

                rooks=(Bitboard.from_square(Square.a8)
                       | Bitboard.from_square(Square.h8)
                       | Bitboard.from_square(Square.a1)
                       | Bitboard.from_square(Square.h1)),

                queens=(Bitboard.from_square(Square.d1)
                        | Bitboard.from_square(Square.d8)),

                kings=(Bitboard.from_square(Square.e8)
                       | Bitboard.from_square(Square.e1))
            ),
            special_moves=SpecialMoveBitboards(
                castling_rooks=self.new_game_by_hand.special_moves.castling_rooks,
                castling_kings=self.new_game_by_hand.special_moves.castling_kings,
                ep_bitboard=Bitboard.from_square(Square.e3)
            ),
            half_move=1,
            turn=False)

        self.white_move_board: FOWChess = (
            FOWChess.new_game().make_move(self.white_move))

        self.black_move: Move = Move(to=Square.d5, frm=Square.d7)

        self.black_move_numpy = np.array(
            [[-4, -2, -3, -5, -6, -3, -2, -4],
             [-1, -1, -1, 0, -1, -1, -1, -1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, -1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 0, 1, 1, 1],
             [4, 2, 3, 5, 6, 3, 2, 4]])

        self.black_move_board_by_hand: FOWChess = FOWChess(
            bitboards=ChessBitboards(
                white=((Bitboard.from_rank(1) | Bitboard.from_rank(2))
                       & ~Bitboard.from_square(Square.e2)
                       | Bitboard.from_square(Square.e4)),

                black=((Bitboard.from_rank(7) | Bitboard.from_rank(8))
                       & ~Bitboard.from_square(Square.d7)
                       | Bitboard.from_square(Square.d5)),

                pawns=((Bitboard.from_rank(7)
                        | Bitboard.from_rank(2)
                        | Bitboard.from_square(Square.e4)
                        | Bitboard.from_square(Square.d5))
                       & ~(Bitboard.from_square(Square.e2)
                           | Bitboard.from_square(Square.d7))),

                knights=(Bitboard.from_square(Square.b1)
                         | Bitboard.from_square(Square.g1)
                         | Bitboard.from_square(Square.b8)
                         | Bitboard.from_square(Square.g8)),

                bishops=(Bitboard.from_square(Square.c1)
                         | Bitboard.from_square(Square.f1)
                         | Bitboard.from_square(Square.c8)
                         | Bitboard.from_square(Square.f8)),

                rooks=(Bitboard.from_square(Square.a8)
                       | Bitboard.from_square(Square.h8)
                       | Bitboard.from_square(Square.a1)
                       | Bitboard.from_square(Square.h1)),

                queens=(Bitboard.from_square(Square.d1)
                        | Bitboard.from_square(Square.d8)),

                kings=(Bitboard.from_square(Square.e8)
                       | Bitboard.from_square(Square.e1))
            ),
            special_moves=SpecialMoveBitboards(
                castling_rooks=self.new_game_by_hand.special_moves.castling_rooks,
                castling_kings=self.new_game_by_hand.special_moves.castling_kings,
                ep_bitboard=Bitboard.from_square(Square.d6)
            ),
            half_move=2,
            turn=True)

        self.black_move_board: FOWChess = (
            self.white_move_board.make_move(self.black_move))


        self.lone_king_and_rook: FOWChess = FOWChess(
            bitboards=ChessBitboards(
                white=(Bitboard.from_square(Square.e1)
                       | Bitboard.from_square(Square.h1)),
                black=Bitboard(0),
                pawns=Bitboard(0),
                knights=Bitboard(0),
                bishops=Bitboard(0),
                rooks=Bitboard.from_square(Square.h1),
                queens=Bitboard(0),
                kings=Bitboard.from_square(Square.e1)
            ),
            special_moves=SpecialMoveBitboards(
                castling_rooks=Bitboard.from_square(Square.h1),
                castling_kings=Bitboard.from_square(Square.e1),
                ep_bitboard=Bitboard(0)
            ),
            half_move=99,
            turn=True)

    def test_new_game(self):
        """Test alt constructor of FOWChess for standard new game position"""
        self.assertEqual(self.new_game_by_hand, FOWChess.new_game())

    def test_equality(self):
        """Test if FOWChess instances are considered equal if their contents are equal"""
        self.assertTrue(self.new_game_by_hand == FOWChess.new_game())
        self.assertFalse(self.new_game_by_hand == self.white_move_board_by_hand)
        self.assertFalse(FOWChess.new_game() == self.white_move_board_by_hand)
        self.assertFalse(self.white_move_board == self.black_move_board)
        self.assertTrue(
                self.white_move_board_by_hand
                == FOWChess.new_game().make_move(self.white_move))
        self.assertTrue(self.black_move_board_by_hand == self.black_move_board)

    def test_from_fow(self):
        """Test if alt constructor from_fow works correctly"""
        self.assertTrue(self.white_move_board_by_hand ==
                        FOWChess.from_fow(FOWChess.new_game(), self.white_move))
        self.assertTrue(self.black_move_board_by_hand ==
                        FOWChess.from_fow(self.white_move_board,
                                          self.black_move))

    def test_half_move_counter(self):
        """Test if half_move_counter increments as expected"""
        self.assertEqual(0, FOWChess.new_game().half_move_counter)
        self.assertEqual(1, self.white_move_board.half_move_counter)
        self.assertEqual(2, self.black_move_board.half_move_counter)

    def test_full_move_number(self):
        """Test if full_move_number increments as expected"""
        self.assertEqual(1, FOWChess.new_game().full_move_number)
        self.assertEqual(1, self.white_move_board.full_move_number)
        self.assertEqual(2, self.black_move_board.full_move_number)

    def test_current_turn(self):
        """Test if the current turn alterantes as expected"""
        self.assertTrue(FOWChess.new_game().current_turn)
        self.assertFalse(self.white_move_board.current_turn)
        self.assertTrue(self.black_move_board.current_turn)

    def test_possible_moves_list(self):
        """Test move generation on a few boards"""
        first_move_set: Set[Move] = {
            # pawns
            Move(frm=Square.a2, to=Square.a3),
            Move(frm=Square.a2, to=Square.a4),
            Move(frm=Square.b2, to=Square.b3),
            Move(frm=Square.b2, to=Square.b4),
            Move(frm=Square.c2, to=Square.c3),
            Move(frm=Square.c2, to=Square.c4),
            Move(frm=Square.d2, to=Square.d3),
            Move(frm=Square.d2, to=Square.d4),
            Move(frm=Square.e2, to=Square.e3),
            Move(frm=Square.e2, to=Square.e4),
            Move(frm=Square.f2, to=Square.f3),
            Move(frm=Square.f2, to=Square.f4),
            Move(frm=Square.g2, to=Square.g3),
            Move(frm=Square.g2, to=Square.g4),
            Move(frm=Square.h2, to=Square.h3),
            Move(frm=Square.h2, to=Square.h4),

            # knights
            Move(frm=Square.g1, to=Square.f3),
            Move(frm=Square.g1, to=Square.h3),
            Move(frm=Square.b1, to=Square.a3),
            Move(frm=Square.b1, to=Square.c3),
        }
        second_move_set: Set[Move] = {
                # pawns
                Move(frm=Square.a7, to=Square.a6),
                Move(frm=Square.a7, to=Square.a5),
                Move(frm=Square.b7, to=Square.b6),
                Move(frm=Square.b7, to=Square.b5),
                Move(frm=Square.c7, to=Square.c6),
                Move(frm=Square.c7, to=Square.c5),
                Move(frm=Square.d7, to=Square.d6),
                Move(frm=Square.d7, to=Square.d5),
                Move(frm=Square.e7, to=Square.e6),
                Move(frm=Square.e7, to=Square.e5),
                Move(frm=Square.f7, to=Square.f6),
                Move(frm=Square.f7, to=Square.f5),
                Move(frm=Square.g7, to=Square.g6),
                Move(frm=Square.g7, to=Square.g5),
                Move(frm=Square.h7, to=Square.h6),
                Move(frm=Square.h7, to=Square.h5),

                # knights
                Move(frm=Square.g8, to=Square.f6),
                Move(frm=Square.g8, to=Square.h6),
                Move(frm=Square.b8, to=Square.a6),
                Move(frm=Square.b8, to=Square.c6),
        }
        third_move_set: Set[Move] = {
                # pawns
                Move(frm=Square.a2, to=Square.a3),
                Move(frm=Square.a2, to=Square.a4),
                Move(frm=Square.b2, to=Square.b3),
                Move(frm=Square.b2, to=Square.b4),
                Move(frm=Square.c2, to=Square.c3),
                Move(frm=Square.c2, to=Square.c4),
                Move(frm=Square.d2, to=Square.d3),
                Move(frm=Square.d2, to=Square.d4),
                Move(frm=Square.f2, to=Square.f3),
                Move(frm=Square.f2, to=Square.f4),
                Move(frm=Square.g2, to=Square.g3),
                Move(frm=Square.g2, to=Square.g4),
                Move(frm=Square.h2, to=Square.h3),
                Move(frm=Square.h2, to=Square.h4),

                # The pawn that moved
                Move(frm=Square.e4, to=Square.e5),
                Move(frm=Square.e4, to=Square.d5),

                # knights
                Move(frm=Square.g1, to=Square.f3),
                Move(frm=Square.g1, to=Square.h3),
                Move(frm=Square.g1, to=Square.e2),
                Move(frm=Square.b1, to=Square.a3),
                Move(frm=Square.b1, to=Square.c3),

                # bishops
                Move(frm=Square.f1, to=Square.e2),
                Move(frm=Square.f1, to=Square.d3),
                Move(frm=Square.f1, to=Square.c4),
                Move(frm=Square.f1, to=Square.b5),
                Move(frm=Square.f1, to=Square.a6),

                # Queens
                Move(frm=Square.d1, to=Square.e2),
                Move(frm=Square.d1, to=Square.f3),
                Move(frm=Square.d1, to=Square.g4),
                Move(frm=Square.d1, to=Square.h5),

                # kings
                Move(frm=Square.e1, to=Square.e2)
        }
        lone_k_and_r_moves: Set[Move] = {
            # king
            Move(frm=Square.e1, to=Square.e2),
            Move(frm=Square.e1, to=Square.f1),
            Move(frm=Square.e1, to=Square.f2),
            Move(frm=Square.e1, to=Square.d1),
            Move(frm=Square.e1, to=Square.d2),

            # rook
            Move(frm=Square.h1, to=Square.g1),
            Move(frm=Square.h1, to=Square.f1),
            Move(frm=Square.h1, to=Square.h2),
            Move(frm=Square.h1, to=Square.h3),
            Move(frm=Square.h1, to=Square.h4),
            Move(frm=Square.h1, to=Square.h5),
            Move(frm=Square.h1, to=Square.h6),
            Move(frm=Square.h1, to=Square.h7),
            Move(frm=Square.h1, to=Square.h8),

            # castling
            Move(frm=Square.e1, to=Square.g1,
                 rook_frm=Square.h1, rook_to=Square.f1)
        }

        self.assertSetEqual(first_move_set, set(FOWChess.new_game().possible_moves_list))
        self.assertSetEqual(second_move_set, set(self.white_move_board.possible_moves_list))
        self.assertSetEqual(third_move_set, set(self.black_move_board.possible_moves_list))
        self.assertSetEqual(lone_k_and_r_moves, set(self.lone_king_and_rook.possible_moves_list))

    def test_make_move(self):
        """Test if making a move works as expected"""
        self.assertTrue(self.white_move_board_by_hand == self.white_move_board)
        self.assertTrue(self.black_move_board_by_hand == self.black_move_board)

    def test_make_random_move(self):
        """Test if make random move works"""
        new: FOWChess = FOWChess.new_game().make_random_move()
        self.assertFalse(FOWChess.new_game() == new)

    def test_castling(self):
        """Test if castling rights are updated as expected"""
        new: FOWChess = self.lone_king_and_rook.make_move(
            Move(frm=Square.e1, to=Square.g1,
                 rook_frm=Square.h1, rook_to=Square.f1))
        self.assertEqual(Bitboard(0), new.special_moves.castling_rooks)
        self.assertEqual(Bitboard(0), new.special_moves.castling_kings)
        self.assertEqual(Bitboard(0), new.special_moves.ep_bitboard)
        self.assertEqual(Bitboard.from_square(Square.g1), new.bitboards.kings)
        self.assertEqual(Bitboard.from_square(Square.f1), new.bitboards.rooks)

    def test_is_over(self):
        """Test if a game is properly detected to be over"""
        self.assertFalse(FOWChess.new_game().is_over)
        self.assertTrue(self.lone_king_and_rook.is_over)

    def test_winner(self):
        """Test if the correct winner is determined"""
        self.assertIsNone(FOWChess.new_game().winner)
        self.assertTrue(self.lone_king_and_rook.winner)

    def test_board_as_numpy(self):
        """Test the conversion to a numpy array representation is as expected"""
        self.assertTrue(np.equal(FOWChess.new_game().to_numpy, self.new_game_numpy).all())
        self.assertTrue(np.equal(self.white_move_board.to_numpy, self.white_move_numpy).all())
        self.assertTrue(np.equal(self.black_move_board.to_numpy, self.black_move_numpy).all())

    def test_black_board(self):
        """Test the conversion to a numpy array representation, from black's POV is as expected"""
        self.assertTrue(
                np.equal(
                        FOWChess.new_game().black_board,
                        np.flipud(self.new_game_numpy)).all())
        self.assertTrue(
                np.equal(
                        self.white_move_board.black_board,
                        np.flipud(self.white_move_numpy)).all())
        self.assertTrue(
                np.equal(self.black_move_board.black_board,
                         np.flipud(self.black_move_numpy)).all())

    def test_white_board(self):
        """Test the conversion to a numpy array representation, from white's POV is as expected"""
        self.assertTrue(
                np.equal(FOWChess.new_game().white_board,
                         self.new_game_numpy).all())
        self.assertTrue(
                np.equal(self.white_move_board.white_board,
                         self.white_move_numpy).all())
        self.assertTrue(
                np.equal(self.black_move_board.white_board,
                         self.black_move_numpy).all())

    def test_black_fog(self):
        """Test visable square generation for black is working"""
        fog = np.zeros((8, 8))
        fog[7] = [1, 1, 1, 1, 1, 1, 1, 1]
        fog[6] = [1, 1, 1, 1, 1, 1, 1, 1]
        fog[5] = [1, 1, 1, 1, 1, 1, 1, 1]
        fog[4] = [1, 1, 1, 1, 1, 1, 1, 1]
        self.assertTrue(np.equal(FOWChess.new_game().visible_to_black, fog).all())
        self.assertTrue(np.equal(self.white_move_board.visible_to_black, fog).all())
        fog[3, 3] = 1
        fog[3, 4] = 1
        fog[2, 7] = 1
        fog[3, 6] = 1
        self.assertTrue(np.equal(self.black_move_board.visible_to_black, fog).all())

    def test_white_fog(self):
        """Test visable square generation for white is working"""
        fog = np.zeros((8, 8))
        fog[7] = [1, 1, 1, 1, 1, 1, 1, 1]
        fog[6] = [1, 1, 1, 1, 1, 1, 1, 1]
        fog[5] = [1, 1, 1, 1, 1, 1, 1, 1]
        fog[4] = [1, 1, 1, 1, 1, 1, 1, 1]
        self.assertTrue(np.equal(FOWChess.new_game().visible_to_white, fog).all())
        fog[3, 4] = 1
        fog[2, 0] = 1
        fog[3, 1] = 1
        fog[3, 7] = 1
        fog[5, 4] = 0
        self.assertTrue(np.equal(self.white_move_board.visible_to_white, fog).all())
        fog[3, 3] = 1
        self.assertTrue(np.equal(self.black_move_board.visible_to_white, fog).all())

    def test_white_foggy_board(self):
        """Test if foggy board from white's POV is working as expected"""
        self.new_game_numpy[0] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.new_game_numpy[1] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.new_game_numpy[2] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.new_game_numpy[3] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.assertTrue(np.equal(self.new_game_numpy, FOWChess.new_game().white_foggy_board).all())

        self.white_move_numpy[0]= [15, 15, 15, 15, 15, 15, 15, 15]
        self.white_move_numpy[1] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.white_move_numpy[2] = [0, 15, 15, 15, 15, 15, 15, 15]
        self.white_move_numpy[3] = [15, 0, 15, 15, 0, 15, 15, 0]
        self.white_move_numpy[5] = [0, 0, 0, 0, 15, 0, 0, 0]
        self.assertTrue(
                np.equal(
                        self.white_move_numpy,
                        self.white_move_board.white_foggy_board).all())

        self.black_move_numpy[0]= [15, 15, 15, 15, 15, 15, 15, 15]
        self.black_move_numpy[1] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.black_move_numpy[2] = [0, 15, 15, 15, 15, 15, 15, 15]
        self.black_move_numpy[3] = [15, 0, 15, -1, 0, 15, 15, 0]
        self.black_move_numpy[5] = [0, 0, 0, 0, 15, 0, 0, 0]
        self.assertTrue(
                np.equal(
                        self.black_move_numpy,
                        self.black_move_board.white_foggy_board).all())

    def test_black_foggy_board(self):
        """Test if foggy board from black's POV is working as expected"""
        self.new_game_numpy[7] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.new_game_numpy[6] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.new_game_numpy[5] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.new_game_numpy[4] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.new_game_numpy = np.flipud(self.new_game_numpy)
        self.assertTrue(
                np.equal(
                        self.new_game_numpy,
                        FOWChess.new_game().black_foggy_board).all())

        self.assertTrue(
                np.equal(self.new_game_numpy,
                         self.white_move_board.black_foggy_board).all())

        self.black_move_numpy[7] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.black_move_numpy[6] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.black_move_numpy[5] = [15, 15, 15, 15, 15, 15, 15, 0]
        self.black_move_numpy[4] = [15, 15, 15, 0, 1, 15, 0, 15]
        self.black_move_numpy = np.flipud(self.black_move_numpy)
        self.assertTrue(
                np.equal(
                        self.black_move_numpy,
                        self.black_move_board.black_foggy_board).all())
