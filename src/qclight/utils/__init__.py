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


def range_fixed_bits(n_bits: "int", fixed_bits: "int | set[int]") -> "Iterator[int]":
    """Loops over all the numbers from 0 to 2**n_bits
    with the bits in the fixed_bits indexes equal to 1.

    All the indexes are considered big endian.

    Example:

        .. code-block:: python

            range_fixed_bits(2, set([1])) # 0b01, 0b11
            range_fixed_bits(3, set([0])) # 0b100, 0b101, 0b110, 0b111
            range_fixed_bits(4, set([2, 3])) # 0b0011, 0b0111, 0b1011, 0b1111

    ```python
    range_fixed_bits(2, set([1])) # 0b01, 0b11
    range_fixed_bits(3, set([0])) # 0b100, 0b101, 0b110, 0b111
    range_fixed_bits(4, set([2, 3])) # 0b0011, 0b0111, 0b1011, 0b1111
    ```

    Args:
        n_bits: number of bits of the values to loop over
        fixed_bits: index or list of indexes of the bits equal to 1, big endian

    Yields:
        all numbers of length n_bits with the fixed_bits equal to 1 and

    Raises:
        OutOfRangeError: if the control_bits indexes are not valid
    """
    if isinstance(fixed_bits, int):
        fixed_bits = set([fixed_bits])
    if any(i >= n_bits for i in fixed_bits):
        raise OutOfRangeError(max_range=n_bits)

    # bit mask with the control bits and switch bit set to 1
    mask = sum(1 << (n_bits - i - 1) for i in fixed_bits)

    out = mask
    yield out

    for _ in range(((2**n_bits) >> len(fixed_bits)) - 1):
        out = (out + 1) | mask
        yield out


def range_fixed_bits_switch(
    n_bits: "int", fixed_bits: "int | set[int]", switch_bit: "int"
) -> "Iterator[tuple[int, int]]":
    """Loops over all the numbers from 0 to 2**n_bits
    with the bits in the fixed_bits indexes equal to 1.

    Each iteration of the loop will return a pair of number.
    The first one will have the bit in the switch_bit position equal to 0.
    The same bit will be 1 in the second element of the pair.

    All the indexes are considered big endian.

    Example:

        .. code-block:: python

            range_fixed_bits_switch(3, set([0]), 1) # (0b100, 0b110), (0b101, 0b111)
            range_fixed_bits_switch(4, set([2, 3]), 1) # (0b0011, 0b0111), (0b1011, 0b1111)
            range_fixed_bits_switch(5, set([0, 1, 2]), 4) # (0b11100, 0b11101), (0b11110, 0b11111)

    ```python
    range_fixed_bits_switch(3, set([0]), 1) # (0b100, 0b110), (0b101, 0b111)
    range_fixed_bits_switch(4, set([2, 3]), 1) # (0b0011, 0b0111), (0b1011, 0b1111)
    range_fixed_bits_switch(5, set([0, 1, 2]), 4) # (0b11100, 0b11101), (0b11110, 0b11111)
    ```

    Args:
        n_bits: number of bits of the values to loop over
        fixed_bits: index or list of indexes of the bits equal to 1, big endian
        switch_bit: index of the bit equal to 0/1 in the pairs, big endian

    Yields:
        all possible pairs of numbers of length n_bits
        with the fixed_bits equal to 1 and the switch_bit equal to 0/1

    Raises:
        OutOfRangeError: if the fixed_bits or switch_bit indexes are not valid
    """
    if isinstance(fixed_bits, int):
        fixed_bits = set([fixed_bits])
    if any(i >= n_bits for i in fixed_bits) or switch_bit >= n_bits:
        raise OutOfRangeError(max_range=n_bits)

    offset = len(fixed_bits) + 1
    # bit mask with the control bits and switch bit set to 1
    mask = sum(1 << (n_bits - i - 1) for i in [*fixed_bits, switch_bit])
    # bit mask with all bits set to 1 except for the switch bit, set to 0
    switch_bit_mask = ~(1 << (n_bits - switch_bit - 1))

    out = mask
    yield out & switch_bit_mask, out

    for _ in range(((2**n_bits) >> offset) - 1):
        out = (out + 1) | mask
        yield out & switch_bit_mask, out
