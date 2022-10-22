"""SumCircuit class"""
import re
import numpy as np
from typing import Iterable
from .circuit import QCLCircuit
from qclight.error import BinaryStringError, PositiveValueError


class SumCircuit(QCLCircuit):
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b
        if a < 0 or b < 0:
            raise PositiveValueError(a if a < 0 else b)
        a_len = a.bit_length() if a > 0 else 1
        b_len = b.bit_length() if b > 0 else 1
        r_len = max(a_len, b_len) + 1
        super().__init__(a_len + b_len + r_len)
        self._initialize_circuit(f"{bin(a)[2:]}{bin(b)[2:]}{'0'*r_len}")
        for i in range(r_len):
            a_idx = a_len - i - 1
            b_idx = a_len + b_len - i - 1
            r_idx = a_len + b_len + r_len - i - 1
            # add the carriage to the next bit of the output if both bits are 1
            if a_len > i and b_len > i:
                self.ccx(a_idx, b_idx, r_idx - 1)
            # xor the value of the bit a if there are still bits to add
            if a_len > i:
                self.cx(a_idx, r_idx)
                # if a is longer than b, consider the possible remaining carriage from the result
                if b_len <= i:
                    self.ccx(b_idx, r_idx, r_idx - 1)
            # xor the value of the bit b if there are still bits to add
            if b_len > i:
                self.cx(b_idx, r_idx)
                # if b is longer than a, consider the possible remaining carriage from the result
                if a_len <= i:
                    self.ccx(a_idx, r_idx, r_idx - 1)

    def sum(self) -> "int":
        """Sums the input numbers and returns the result.
        Runs the quantum circuit and return the certain output as an integer.

        Returns:
            result obtained by summing the input numbers
        """
        self.run()
        sum_state = np.where(self.result == 1)[0][0]
        a_len = self.a.bit_length() if self.a > 0 else 1
        b_len = self.b.bit_length() if self.b > 0 else 1
        tot_len = a_len + b_len + max(a_len, b_len) + 1
        bin_str = f"{sum_state:0{tot_len}b}"[a_len + b_len :]
        return int(bin_str, 2)

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
