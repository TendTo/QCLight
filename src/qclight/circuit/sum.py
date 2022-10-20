import re
from typing import Iterable
from .circuit import QCLCircuit
from qclight.error import BinaryStringError, PositiveValueError


class SumCircuit(QCLCircuit):
    def __init__(self, a: int, b: int) -> None:
        if a < 0 or b < 0:
            raise PositiveValueError(a if a < 0 else b)
        a_len = a.bit_length()
        b_len = b.bit_length()
        r_len = max(a_len, b_len) + 1
        super().__init__(a_len + b_len + r_len)

    def __get_one_position_string(self, val: str) -> Iterable[int]:
        """Produces an iterable over the indices of the bits that are set to 1 in the binary representation of the number.

        Args:
            val: input number

        Returns:
            list of indices of the bits that are set to 1 in the binary representation of the number
        """
        if re.match(r"^[01]+$", val) is None:
            raise BinaryStringError(val)
        for i, bit in enumerate(val[::-1]):
            if bit == "1":
                yield i

    def __get_one_position_int(self, val: int) -> Iterable[int]:
        """Produces an iterable over the indices of the bits that are set to 1 in the binary representation of the number.

        Args:
            val: input number

        Returns:
            list of indices of the bits that are set to 1 in the binary representation of the number
        """
        for i in range(self.n):
            if val & (1 << i):
                yield i

    def add(self, val: int) -> None:
        raise NotImplementedError()
