"""IGate class"""
import numpy as np
import numpy.typing as npt
from .gate import Gate


class IGate(Gate):
    """Identity gate.
    It does not change the state of a qubit.

    .. math::
        I = \\begin{bmatrix}
        1 & 0 \\\\
        0 & 1
        \\end{bmatrix}
    """

    @property
    def matrix(self) -> "npt.NDArray[np.float64]":
        return self.__class__.I

    def __str__(self):
        return "I"
