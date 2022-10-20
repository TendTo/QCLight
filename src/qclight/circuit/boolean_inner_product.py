from .circuit import QCLCircuit


class BooleanInnerProductCircuit(QCLCircuit):
    def __init__(self, n: int) -> None:
        super().__init__(n)
        raise NotImplementedError()
