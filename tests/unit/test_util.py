# pylint: disable=missing-function-docstring,too-few-public-methods,redefined-outer-name
"""Test circuit package."""
import pytest
from qclight.utils import (
    bitstring_to_int,
    BinaryStringError,
    extract_bits,
)


class TestUtil:
    """Tests the util package."""

    def test_bitstring_to_int(self):
        res = bitstring_to_int("010101")
        assert res == 0b10101

    def test_bitstring_to_int_start(self):
        res = bitstring_to_int("010101", start=3)
        assert res == 0b101

    def test_bitstring_to_int_end(self):
        res = bitstring_to_int("010101", end=3)
        assert res == 0b10

    def test_bitstring_to_int_start_end(self):
        res = bitstring_to_int("010101", start=1, end=4)
        assert res == 0b101

    def test_bitstring_to_int_invalid(self):
        with pytest.raises(BinaryStringError):
            bitstring_to_int("invalid")

    def test_extract_bits_single(self):
        for i in (0, 2, 3):
            res = extract_bits(0b1011, i)
            assert res == 0b1
        res = extract_bits(0b1011, 1)
        assert res == 0b0

    def test_extract_bits_multiple(self):
        res = extract_bits(0b1011, [0, 2, 3])
        assert res == 0b111
        res = extract_bits(0b1011, [3, 1, 1])
        assert res == 0b100
