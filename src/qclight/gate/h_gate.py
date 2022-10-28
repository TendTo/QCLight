"""HGate class"""
import numpy as np
import numpy.typing as npt
from .gate import Gate


class HGate(Gate):
    """Hadamard gate.
    It rotates a qubit and puts it in a state of superpositions.

    .. math::
        H = \\frac{1}{\\sqrt{2}} \\begin{bmatrix}
        1 & 1 \\\\
        1 & -1
        \\end{bmatrix}
    """

    H: npt.NDArray[np.float64] = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])

    @property
    def matrix(self) -> npt.NDArray[np.float64]:
        return self.__class__.H

    def __str__(self):
        return "H"
