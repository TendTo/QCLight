"""Many of the functions in ths library apply some kind of validation
on the input parameters.
If the inputs are not valid, they may raise an exception.

To make as clear as possible what went wrong, this package includes
a number of custom exceptions that try to be as explicit as possible.
"""


class BinaryStringError(ValueError):
    """Raised when the string received is not the string representation of a number in binary."""

    def __init__(self, invalid_string: str) -> None:
        super().__init__(f"Expected a binary string, received '{invalid_string}'")


class PowerOfTwoError(ValueError):
    """Raised when the number received is not a power of 2."""

    def __init__(self, invalid_number: int) -> None:
        super().__init__(f"Expected a power of two, received '{invalid_number}'")


class PowerOfTwoLengthError(ValueError):
    """Raised when the length of the vector received is not a power of 2."""

    def __init__(self, invalid_number: int) -> None:
        super().__init__(
            f"Expected a vector with a length of a power of two, received '{invalid_number}'"
        )


class PositiveValueError(ValueError):
    """Raised when the value received is not positive.
    It means it is less or equal to 0.
    """

    def __init__(self, invalid_number: int) -> None:
        super().__init__(f"Expected a positive value, received '{invalid_number}'")


class BitValueError(ValueError):
    """Raised when the value received is not a single bit.
    The value expected was either 0 or 1.
    """

    def __init__(self, invalid_number: int) -> None:
        super().__init__(f"Expected a '0' or '1' value, received '{invalid_number}'")
