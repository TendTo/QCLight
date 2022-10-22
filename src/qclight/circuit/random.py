"""RandomCircuit class"""
from .circuit import QCLCircuit


class RandomCircuit(QCLCircuit):
    """Using the true randomness of the qubits,
    it is possible to generate a true random number between 0 and 2^n - 1.

    It is sufficient to use apply the :attr:`~qclight.gates.gates.Gate.H` gate to n qubits
    to produce a uniform superposition of all possible states.
    """

    def __init__(self, n: int) -> None:
        super().__init__(n)
        self.h(list(range(n)))
