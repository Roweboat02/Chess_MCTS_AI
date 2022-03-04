"""
test_bitboards.py
Tests for bitboard functionality.

Author: Noah Rowe
Date: 2022/02/22
Last Modified: 2022/02/23
    Added docstrings
"""
from unittest import TestCase

import numpy as np

from fog_of_war.helper_functions import reduce_with_bitwise_or
from fog_of_war.bitboard import Bitboard
from fog_of_war.square import Square


class TestBitboard(TestCase):
    """Bitboard tests"""
    def setUp(self) -> None:
        """Set up"""
        self.empty: Bitboard = Bitboard(0)

        self.full: Bitboard = Bitboard(0xff_ff_ff_ff_ff_ff_ff_ff)

        self.rank_1: Bitboard = Bitboard(0xff)
        self.rank_8: Bitboard = Bitboard(0xff << (8 * 7))

        self.file_1: Bitboard = Bitboard(0x0101_0101_0101_0101)
        self.file_8: Bitboard = Bitboard(0x0101_0101_0101_0101 << 7)

        self.first_square: Bitboard = Bitboard(1)

    def test_bitboard_to_numpy(self):
        """Test Bitboard to numpy array conversion"""
        numpy_empty: np.ndarray = np.zeros((8, 8))

        numpy_full: np.ndarray = np.ones((8, 8))

        numpy_rank_1: np.ndarray = np.zeros((8, 8))
        numpy_rank_1[7] = 1

        numpy_file_1: np.ndarray = np.zeros((8, 8))
        numpy_file_1[:, 0] = 1

        numpy_file_8: np.ndarray = np.fliplr(numpy_file_1)
        numpy_rank_8: np.ndarray = np.flipud(numpy_rank_1)
        self.assertTrue(np.equal(self.empty.to_numpy(), numpy_empty).all())
        self.assertTrue(np.equal(self.full.to_numpy(), numpy_full).all())

        self.assertTrue(np.equal(self.rank_1.to_numpy(), numpy_rank_1).all())
        self.assertTrue(np.equal(self.file_1.to_numpy(), numpy_file_1).all())

        self.assertTrue(np.equal(self.rank_8.to_numpy(), numpy_rank_8).all())
        self.assertTrue(np.equal(self.file_8.to_numpy(), numpy_file_8).all())

    def test_from_rank(self):
        """Test Bitboard alternate constructor "from_rank" """
        self.assertEqual(Bitboard.from_rank(1), self.rank_1)
        self.assertEqual(Bitboard.from_rank(8), self.rank_8)
        self.assertEqual(reduce_with_bitwise_or(
            Bitboard.from_rank(1),
            Bitboard.from_rank(2),
            Bitboard.from_rank(3),
            Bitboard.from_rank(4),
            Bitboard.from_rank(5),
            Bitboard.from_rank(6),
            Bitboard.from_rank(7),
            Bitboard.from_rank(8)),
            self.full)

    def test_from_file(self):
        """Test Bitboard alternate constructor "from_file" """
        self.assertEqual(Bitboard.from_file(1), self.file_1)
        self.assertEqual(Bitboard.from_file(8), self.file_8)
        self.assertEqual(reduce_with_bitwise_or(
            Bitboard.from_file(1),
            Bitboard.from_file(2),
            Bitboard.from_file(3),
            Bitboard.from_file(4),
            Bitboard.from_file(5),
            Bitboard.from_file(6),
            Bitboard.from_file(7),
            Bitboard.from_file(8)),
            self.full)

    def test_from_square(self):
        """Test Bitboard alternate constructor "from_square" """
        self.assertEqual(Bitboard.from_square(Square(1)), self.first_square)
        self.assertEqual(
            reduce_with_bitwise_or(*(Bitboard.from_square(Square(i)) for i in range(1, 9))),
            self.rank_1)
        self.assertEqual(
            reduce_with_bitwise_or(*(Bitboard.from_square(Square(i)) for i in range(57, 65))),
            self.rank_8)
        self.assertEqual(
            reduce_with_bitwise_or(*(Bitboard.from_square(Square(i)) for i in range(1, 58, 8))),
            self.file_1)
        self.assertEqual(
            reduce_with_bitwise_or(*(Bitboard.from_square(Square(i)) for i in range(8, 65, 8))),
            self.file_8)
