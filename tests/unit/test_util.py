# pylint: disable=missing-function-docstring,too-few-public-methods,redefined-outer-name
"""Test circuit package."""
import pytest
from qclight.utils import bitstring_to_int, BinaryStringError


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
