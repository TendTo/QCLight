from .circuit import QCLCircuit


class BellCircuit(QCLCircuit):
    def __init__(self, n: int) -> None:
        super().__init__(n)
        raise NotImplementedError()
