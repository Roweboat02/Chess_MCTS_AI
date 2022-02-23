from typing import Tuple
from unittest import TestCase
from square import Square

class TestSquare(TestCase):
    def setUp(self) -> None:
        self.a1: Tuple[int,int] = 1,1
        self.b2: Tuple[int,int] = 2,2
        self.c3: Tuple[int,int] = 3,3
        self.d4: Tuple[int,int] = 4,4
        self.e5: Tuple[int,int] = 5,5
        self.f6: Tuple[int,int] = 6,6
        self.g7: Tuple[int,int] = 7,7
        self.h8: Tuple[int,int] = 8,8

        self.a8: Tuple[int,int] = 8,1
        self.b7: Tuple[int,int] = 7,2
        self.c6: Tuple[int,int] = 6,3
        self.d5: Tuple[int,int] = 5,4
        self.e4: Tuple[int,int] = 4,5
        self.f3: Tuple[int,int] = 3,6
        self.g2: Tuple[int,int] = 2,7
        self.h1: Tuple[int,int] = 1,8

        self.sqrs_as_ranks = [i for i in range(1,9) for j in range(1,9)]

        self.sqrs_as_files = [j for i in range(1,9) for j in range(1,9)]

    def test_square_values(self):
        self.assertLess(Square.a1.value, Square.a2.value)
        self.assertLess(Square.b1.value, Square.a2.value)
        self.assertLess(Square.a8.value, Square.h8.value)

    def test_diagonals(self):
        self.assertEqual(self.a1, (Square.a1.rank, Square.a1.file))
        self.assertEqual(self.b2, (Square.b2.rank, Square.b2.file))
        self.assertEqual(self.c3, (Square.c3.rank, Square.c3.file))
        self.assertEqual(self.d4, (Square.d4.rank, Square.d4.file))
        self.assertEqual(self.e5, (Square.e5.rank, Square.e5.file))
        self.assertEqual(self.f6, (Square.f6.rank, Square.f6.file))
        self.assertEqual(self.g7, (Square.g7.rank, Square.g7.file))
        self.assertEqual(self.h8, (Square.h8.rank, Square.h8.file))

        self.assertEqual(self.a8, (Square.a8.rank, Square.a8.file))
        self.assertEqual(self.b7, (Square.b7.rank, Square.b7.file))
        self.assertEqual(self.c6, (Square.c6.rank, Square.c6.file))
        self.assertEqual(self.d5, (Square.d5.rank, Square.d5.file))
        self.assertEqual(self.e4, (Square.e4.rank, Square.e4.file))
        self.assertEqual(self.f3, (Square.f3.rank, Square.f3.file))
        self.assertEqual(self.g2, (Square.g2.rank, Square.g2.file))
        self.assertEqual(self.h1, (Square.h1.rank, Square.h1.file))

    def test_ranks(self):
        self.assertEqual(self.sqrs_as_ranks, [i.rank for i in Square])

    def test_files(self):
        self.assertEqual(self.sqrs_as_files, [i.file for i in Square])
