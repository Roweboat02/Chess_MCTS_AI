from unittest import TestCase
import numpy as np
from fog_of_war.fog_of_war_chess import FOWChess

"""
Broke FOWChess up a bit, some responsibility moved to FOWBoard.
Haven't had a chance to change FOWChess's tests of that functionality to FOWBoard.
So they're just copied and pasted here for now.

-Noah 2022/03/21
"""


class TestFOWBoard(TestCase):
    def test_foggy_board(self):
        self.fail()

    def test_visible_to_color(self):
        self.fail()
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

        self.white_move_numpy[0] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.white_move_numpy[1] = [15, 15, 15, 15, 15, 15, 15, 15]
        self.white_move_numpy[2] = [0, 15, 15, 15, 15, 15, 15, 15]
        self.white_move_numpy[3] = [15, 0, 15, 15, 0, 15, 15, 0]
        self.white_move_numpy[5] = [0, 0, 0, 0, 15, 0, 0, 0]
        self.assertTrue(
            np.equal(
                self.white_move_numpy,
                self.white_move_board.white_foggy_board).all())

        self.black_move_numpy[0] = [15, 15, 15, 15, 15, 15, 15, 15]
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
