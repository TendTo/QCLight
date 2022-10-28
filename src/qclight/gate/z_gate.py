"""ZGate class"""
import numpy as np
import numpy.typing as npt
from .gate import Gate


class ZGate(Gate):
    """Z gate.
    It rotates a qubit by :math:`\\pi` radians around the z-axis.

    .. math::
        Z = \\begin{bmatrix}
        1 & 0 \\\\
        0 & -1
        \\end{bmatrix}
    """

    Z: npt.NDArray[np.float64] = np.array([[1, 0], [0, -1]])

    @property
    def matrix(self) -> npt.NDArray[np.float64]:
        return self.__class__.Z

    def __str__(self):
        return "Z"
