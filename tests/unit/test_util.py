# pylint: disable=missing-function-docstring,too-few-public-methods,redefined-outer-name
"""Test util package."""
import pytest
from qclight.utils import (
    BinaryStringError,
    OutOfRangeError,
    bitstring_to_int,
    extract_bits,
    range_fixed_bits_switch,
    range_fixed_bits,
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

    def test_range_fixed_bits_single_first(self):
        res = list(range_fixed_bits(3, 0))
        assert res == [0b100, 0b101, 0b110, 0b111]

    def test_range_fixed_bits_single_middle(self):
        res = list(range_fixed_bits(2, 1))
        assert res == [0b01, 0b11]

    def test_range_fixed_bits_single_invalid(self):
        with pytest.raises(OutOfRangeError):
            list(range_fixed_bits(3, 3))

    def test_range_fixed_bits_multiple_sequence(self):
        res = list(range_fixed_bits(3, set([0, 1])))
        assert res == [0b110, 0b111]

    def test_range_fixed_bits_multiple_mixed(self):
        res = list(range_fixed_bits(5, set([1, 3, 0])))
        assert res == [0b11010, 0b11011, 0b11110, 0b11111]

    def test_range_fixed_bits_multiple_invalid(self):
        with pytest.raises(OutOfRangeError):
            list(range_fixed_bits(3, set([0, 1, 2, 3])))

    def test_range_fixed_bits_switch_single_sequence(self):
        res = list(range_fixed_bits_switch(3, 0, 1))
        assert res == [(0b100, 0b110), (0b101, 0b111)]

    def test_range_fixed_bits_switch_single_mixed(self):
        res = list(range_fixed_bits_switch(4, 3, 1))
        assert res == [
            (0b0001, 0b0101),
            (0b0011, 0b0111),
            (0b1001, 0b1101),
            (0b1011, 0b1111),
        ]

    def test_range_fixed_bits_switch_single_invalid_fixed(self):
        with pytest.raises(OutOfRangeError):
            list(range_fixed_bits_switch(3, 3, 0))

    def test_range_fixed_bits_switch_single_invalid_switch(self):
        with pytest.raises(OutOfRangeError):
            list(range_fixed_bits_switch(3, 0, 3))

    def test_range_fixed_bits_switch_multiple_sequence(self):
        res = list(range_fixed_bits_switch(3, set([0, 1]), 2))
        assert res == [(0b110, 0b111)]

    def test_range_fixed_bits_switch_multiple_mixed(self):
        res = list(range_fixed_bits_switch(4, set([3, 1]), 2))
        assert res == [(0b0101, 0b0111), (0b1101, 0b1111)]

    def test_range_fixed_bits_switch_multiple_invalid_fixed(self):
        with pytest.raises(OutOfRangeError):
            list(range_fixed_bits_switch(3, set([2, 3]), 0))

    def test_range_fixed_bits_switch_multiple_invalid_switch(self):
        with pytest.raises(OutOfRangeError):
            list(range_fixed_bits_switch(3, set([0, 1]), 3))
