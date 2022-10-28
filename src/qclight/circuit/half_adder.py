"""HalfAdderCircuit class"""
import numpy as np
from qclight.error import BitValueError
from .circuit import QCLCircuit


class HalfAdderCircuit(QCLCircuit):
    """Half adder circuit.
    Allows to sum two bits and return the result, as well as the carry bit.

    | a | b | sum | carry |
    |:-:|:-:|:---:|:-----:|
    | 0 | 0 |  0  |   0   |
    | 0 | 1 |  1  |   0   |
    | 1 | 0 |  1  |   0   |
    | 1 | 1 |  0  |   1   |

    .. table:: Truth table of the half adder circuit.

        === === ===== =======
         a   b   sum   carry
        === === ===== =======
         0   0    0      0
         0   1    1      0
         1   0    1      0
         1   1    0      1
        === === ===== =======
    """

    def __init__(self, a: "int", b: "int") -> "None":
        if a not in (0, 1) or b not in (0, 1):
            raise BitValueError(a if a not in (0, 1) else b)
        self.a = a
        self.b = b
        super().__init__(4)
        self.initialize_circuit(f"{a}{b}00")
        # xor between a and b
        self.cx(0, 3)
        self.cx(1, 3)
        # and between a and b
        self.ccx(0, 1, 2)

    def sum(self) -> "int":
        """Sums the input numbers and returns the result.
        Runs the quantum circuit and return the certain output as an integer.

        Returns:
            result obtained by summing the input numbers
        """
        self.run()
        sum_state = np.where(self.result == 1)[0][0]
        bin_str = f"{sum_state:04b}"[2:]
        return int(bin_str, 2)
