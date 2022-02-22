from __future__ import annotations
import numpy as np
from square import Square

class Bitboard(int):
    square_masks = {sqr: 1 << (sqr.value-1) for sqr in Square}
    rank_masks = {rank:0xff << ((rank-1) * 8) for rank in range(1,9)}
    file_masks = {file:0x0101_0101_0101_0101 << (file-1) for file in range(1,9)}

    def __new__(cls, bb: int):
        """
        64bit uint bitboard.
        Bitboard must be a positave interger representable as 64 bits."""
        if not (bb.bit_length() <= 64 or bb > -1):
            raise ValueError("Must be a positave interger representable as 64 bits")
        return super(Bitboard, cls).__new__(cls, bb)

    def bitboard_to_numpy(self) -> np.ndarray:
        """
        Convert bitboard from int representation to representing as an 8x8 numpy array of 1's and 0's
        @return arr:np.ndarray - An 8x8 numpy array (dtype=np.int16)
        """
        try:
            bb_bytes = (int(self) >> np.arange(0, 57, 8, dtype=np.uint64)).astype(np.uint8)
        except OverflowError:
            as_string = format(self, '064b')
            bb_bytes = np.array([int(as_string[i:i+8]) for i in range(0,64,8)], dtype=np.uint8)

        return np.flipud(np.unpackbits(bb_bytes , bitorder="little").reshape(8, 8).astype(np.int16))

    @classmethod
    def from_rank(cls, rank_num: int) -> Bitboard:
        """
        Create a bitboard with the specified rank set to 1.
        @param rank_num:int - integer between 1 and 8 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with rank (row) rankNum 1, and all else 0.
        """
        if not 0<rank_num<9:
            raise ValueError("Must be a positave interger between 1 and 8 (inclusive)")
        return cls(cls.rank_masks[rank_num])

    @classmethod
    def from_file(cls, file_num: int) -> Bitboard:
        """
        Create a bitboard with the specified file set to 1.
        @param file_num:int - integer between 1 and 8 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with file (col) fileNum 1, and all else 0.
        """
        if not 0<file_num<9:
            raise ValueError("Must be a positave interger between 1 and 8 (inclusive)")
        return cls(cls.file_masks[file_num])

    @classmethod
    def from_square(cls, square_num: Square) -> Bitboard:
        """
        Create a bitboard with the specified square set to 1, numbered rank*8 + file.
        @param square_num:Square - item from enum Square used as an int between 1 and 64 (inclusive)
        @return bb:int - int that can be interpreted as an 8x8 bitboard with square squareNum, and all else 0.
        """
        return cls(cls.square_masks[square_num])
