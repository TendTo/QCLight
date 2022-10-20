from .circuit import QCLCircuit


class RandomCircuit(QCLCircuit):
    def __init__(self, n: int) -> None:
        super().__init__(n)
        raise NotImplementedError()
