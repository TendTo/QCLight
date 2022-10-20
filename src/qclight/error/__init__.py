"""Error package.
All the errors that can arise in the simulator.
"""


class BinaryStringError(Exception):
    """Raised when the string received is not the string representation of a number in binary."""

    def __init__(self, invalid_string: str) -> None:
        super().__init__(f"Expected a binary string, received '{invalid_string}'")


class PowerOfTwoError(Exception):
    """Raised when the number received is not a power of 2."""

    def __init__(self, invalid_number: int) -> None:
        super().__init__(f"Expected a power of two, received '{invalid_number}'")


class PowerOfTwoLengthError(Exception):
    """Raised when the length of the vector received is not a power of 2."""

    def __init__(self, invalid_number: int) -> None:
        super().__init__(
            f"Expected a vector with a length of a power of two, received '{invalid_number}'"
        )


class PositiveValueError(Exception):
    """Raised when the value received is not positive.
    It means it is less or equal to 0.
    """

    def __init__(self, invalid_number: int) -> None:
        super().__init__(f"Expected a positive value, received '{invalid_number}'")
