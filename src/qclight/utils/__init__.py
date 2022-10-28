"""Utility functions used by QCLight.
These are mostly math and bit manipulation functions.
"""


import re
from typing import Iterator
from qclight.error import BinaryStringError, OutOfRangeError


def bitstring_to_int(
    bitstring: "str", start: "int" = 0, end: "int | None" = None
) -> "int":
    """Convert a bitstring to an integer.

    Args:
        bitstring: bitstring to convert
        start: start index of the bitstring
        end: end index of the bitstring

    Returns:
        integer representation of the bitstring
    """
    if re.match(r"^[01]+$", bitstring) is None:
        raise BinaryStringError(bitstring)
    if end is None:
        end = len(bitstring)
    return int(bitstring[start:end], 2)


def extract_bits(number: "int", idx: "int | list[int]") -> "int":
    """Extracts the bits with index idx (or in the list idx)
    from the binary representation of number.
    The bits are then used to build  a new number,
    in the order they appear in the list, big endian.

    Example:

        .. code-block:: python

            extract_bits(0b1011, 0) # 1
            extract_bits(0b1011, 1) # 0
            extract_bits(0b1011, [1, 2, 3]) # 0b011 -> 3
            extract_bits(0b1011, [3, 1, 1]) # 0b100 -> 4

    ```python
    extract_bits(0b1011, 0) # 1
    extract_bits(0b1011, 1) # 0
    extract_bits(0b1011, [1, 2, 3]) # 0b011 -> 3
    extract_bits(0b1011, [3, 1, 1]) # 0b100 -> 4
    ```

    Args:
        number: number in binary where the bits are extracted from
        idx: index or list of indexes of the bits to extract, big endian

    Returns:
        a number build using the extracted bits
    """
    n = number.bit_length()
    if isinstance(idx, int):
        return number >> (n - idx - 1) & 1

    bits = 0
    for i in idx:
        bit = (number >> (n - i - 1)) & 1
        bits = (bits << 1) | bit
    return bits
