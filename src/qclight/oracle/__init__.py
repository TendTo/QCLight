from typing import Iterable
from qclight.circuit import QCLCircuit


class BooleanOracle:
    def __init__(self, n: int, sol: Iterable[int]) -> None:
        circuit = QCLCircuit(n)
