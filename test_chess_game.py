from unittest import TestCase
import chess_game as cg
import chess


class TestChess(TestCase):
    def setUp(self):
        self.game = cg.Chess()

    def test_check_color(self):
        self.assertIsTrue(self.game.check_color())
        self.assertIsTrue(self.game.check_color(True))
        self.assertIsFalse(self.game.check_color(False))
        self.game.make_move(chess.Move.from_uci('a3'))
        self.assertIsFalse(self.game.check_color())

    def test_copy(self):
        self.game.copy()

    def test_fog(self):
        self.assertIsTrue(np.equal(self.game.fog,
         np.array([[i for _ in range(8)] for i in [0,0,0,0,0,1,1,1]])))

    def test_game_array(self):
        self.game.game_array

    def test_make_move(self):
        self.fail()

    def test_make_random_move(self):
        self.fail()

    def test_make_questionable_move(self):
        self.fail()


    def test_reset(self):
        pass
