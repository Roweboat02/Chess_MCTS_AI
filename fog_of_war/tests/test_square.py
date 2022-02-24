"""
test_square.py
Tests for Square (of a chess board)'s functionality.

Author: Noah Rowe
Date: 2022/02/22
Last Modified: 2022/02/23
    Added docstrings
"""
from typing import List
from unittest import TestCase
from fog_of_war.square import Square


class TestSquare(TestCase):
    """
    Square tests
    """

    def setUp(self) -> None:
        """Set up"""
        self.sqrs_as_ranks: List[int] = [i for i in range(1, 9) for _ in range(1, 9)]

        self.sqrs_as_files: List[int] = [j for _ in range(1, 9) for j in range(1, 9)]

    def test_square_values(self):
        """Test to make sure value is as expected"""
        self.assertLess(Square.a1.value, Square.a2.value)
        self.assertLess(Square.b1.value, Square.a2.value)
        self.assertLess(Square.a8.value, Square.h8.value)

    def test_ranks(self):
        """Test that all squares have the expected rank"""
        self.assertEqual(self.sqrs_as_ranks, [i.rank for i in Square])

    def test_files(self):
        """Test that all squares have the expected file"""
        self.assertEqual(self.sqrs_as_files, [i.file for i in Square])
