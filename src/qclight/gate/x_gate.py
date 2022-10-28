"""XGate class"""
import numpy as np
import numpy.typing as npt
from .gate import Gate


class XGate(Gate):
    """Negation gate.
    It negates the state of a qubit.

    .. math::
        X = \\begin{bmatrix}
        0 & 1 \\\\
        1 & 0
        \\end{bmatrix}
    """

    X: "npt.NDArray[np.float64]" = np.array([[0, 1], [1, 0]])

    @property
    def matrix(self) -> "npt.NDArray[np.float64]":
        return self.__class__.X

    def __str__(self):
        return "X"
