"""BooleanInnerProductCircuit class."""
import numpy as np
from qclight.error import PositiveValueError
from .circuit import QCLCircuit


class BooleanInnerProductCircuit(QCLCircuit):
    """The boolean inner product is defined as
    the bitwise AND of the two vectors
    followed by the XOR bit by bit of the result.

    .. math::

        \\begin{align}
        x \\cdot y =
        \\underbrace{(x_1 \\land y_1) \\oplus (x_2 \\land y_2) \\oplus
        \\dots
        \\oplus (x_n \\land y_n)}_{n}
        \\end{align}
    """

    def __init__(self, a: "int", b: "int") -> "None":
        if a < 0 or b < 0:
            raise PositiveValueError(a if a < 0 else b)
        a_len = a.bit_length() if a > 0 else 1
        b_len = b.bit_length() if b > 0 else 1
        r_idx = a_len + b_len
        super().__init__(a_len + b_len + 1)
        self._initialize_circuit(f"{a:0{a_len}b}{b:0{b_len}b}0")
        for i in range(min(a_len, b_len)):
            a_idx = a_len - i - 1
            b_idx = a_len + b_len - i - 1
            self.ccx(a_idx, b_idx, r_idx)

    def inner_product(self) -> "bool":
        """Computes the boolean inner product of the input vectors
        and returns the result.

        Returns:
            result obtained by computing the boolean inner product
        """
        self.run()
        idx = np.where(self.result == 1)[0][0]
        return bool(idx & 1)
