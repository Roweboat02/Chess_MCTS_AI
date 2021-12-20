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

    def test_game_to_array(self):
        self.fail()

    def test_generate_fog(self):
        self.fail()

    def test_possible_next_moves(self):
        self.fail()

    def test_has_winner(self):
        self.fail()

    def test_make_move(self):
        self.fail()

    def test_make_random_move(self):
        self.fail()

    def test_make_questionable_move(self):
        self.fail()

    def test_copy(self):
        self.fail()

    def test_reset(self):
        self.fail()
