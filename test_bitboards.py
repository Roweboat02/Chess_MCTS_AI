from functools import reduce
from unittest import TestCase
from bitboard import Bitboard
from square import Square
import numpy as np


class TestBitboard(TestCase):
    def setUp(self) -> None:
        self.empty:Bitboard = Bitboard(0)

        self.full:Bitboard = Bitboard(0xff_ff_ff_ff_ff_ff_ff_ff)

        self.rank_1:Bitboard = Bitboard(0xff)
        self.rank_8:Bitboard = Bitboard(0xff << (8*7))

        self.file_1:Bitboard = Bitboard(0x0101_0101_0101_0101)
        self.file_8:Bitboard = Bitboard(0x0101_0101_0101_0101 << 7)

        self.first_square:Bitboard = Bitboard(1)

        self.numpy_empty:np.ndarray = np.zeros((8,8))

        self.numpy_full:np.ndarray = np.ones((8,8))

        self.numpy_rank_1:np.ndarray = np.zeros((8,8))
        self.numpy_rank_1[7] = 1

        self.numpy_file_1:np.ndarray = np.zeros((8,8))
        self.numpy_file_1[:,0] = 1

        self.numpy_file_8:np.ndarray = np.fliplr(self.numpy_file_1)
        self.numpy_rank_8:np.ndarray = np.flipud(self.numpy_rank_1)

    def test_bitboard_to_numpy(self):
        self.assertTrue(np.equal(self.empty.bitboard_to_numpy(), self.numpy_empty).all())
        self.assertTrue(np.equal(self.full.bitboard_to_numpy(), self.numpy_full).all())

        self.assertTrue(np.equal(self.rank_1.bitboard_to_numpy(), self.numpy_rank_1).all())
        self.assertTrue(np.equal(self.file_1.bitboard_to_numpy(), self.numpy_file_1).all())

        self.assertTrue(np.equal(self.rank_8.bitboard_to_numpy(), self.numpy_rank_8).all())
        self.assertTrue(np.equal(self.file_8.bitboard_to_numpy(), self.numpy_file_8).all())

    def test_from_rank(self):
        self.assertEqual(Bitboard.from_rank(1), self.rank_1)
        self.assertEqual(Bitboard.from_rank(8), self.rank_8)
        self.assertEqual(
                Bitboard.from_rank(1)|Bitboard.from_rank(2)|Bitboard.from_rank(3)|Bitboard.from_rank(4)|Bitboard.from_rank(5)|Bitboard.from_rank(6)|Bitboard.from_rank(7)|Bitboard.from_rank(8),
                self.full)

    def test_from_file(self):
        self.assertEqual(Bitboard.from_file(1), self.file_1)
        self.assertEqual(Bitboard.from_file(8), self.file_8)
        self.assertEqual(
                Bitboard.from_file(1)|Bitboard.from_file(2)|Bitboard.from_file(3)|Bitboard.from_file(4)|Bitboard.from_file(5)|Bitboard.from_file(6)|Bitboard.from_file(7)|Bitboard.from_file(8),
                self.full)

    def test_from_square(self):
        self.assertEqual(Bitboard.from_square(Square(1)), self.first_square)
        self.assertEqual(
                Bitboard(reduce(lambda a,b: a|b, (Bitboard.from_square(Square(i)) for i in range(1,9)))),
                self.rank_1)
        self.assertEqual(
                Bitboard(reduce(lambda a,b: a|b, (Bitboard.from_square(Square(i)) for i in range(57,65)))),
                self.rank_8)
        self.assertEqual(
                Bitboard(reduce(lambda a,b: a|b, (Bitboard.from_square(Square(i)) for i in range(1,58,8)))),
                self.file_1)
        self.assertEqual(
                Bitboard(reduce(lambda a,b: a|b, (Bitboard.from_square(Square(i)) for i in range(8,65,8)))),
                self.file_8)
