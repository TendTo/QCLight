"""QCLCircuit class"""
from typing import Iterable
import numpy as np
import numpy.typing as npt
from qclight.gate import HGate, XGate, IGate
from qclight.visualizer.circuit_visualizer import CircuitVisualizer
from .circuit import QCLCircuit

FloatNDArray = npt.NDArray[np.float64]


class QCLVisualCircuit(QCLCircuit):
    """Quantum circuit used for a generic computation.
    This subclass of :class:`~qclight.circuit.circuit.QCLCircuit` adds
    visualization capabilities to the circuit.
    To print the circuit, simply call the :meth:`__str__` method.
    """

    def __init__(self, state: "str | list[float] | int") -> "None":
        super().__init__(state)
        self._visualizer = CircuitVisualizer(self.n)

    @property
    def n(self) -> "int":
        return self._n

    @n.setter
    def n(self, n: "int") -> "None":
        self._n = n
        self._identity = IGate().matrix_of_size(n)
        self._visualizer = CircuitVisualizer(n)

    def _initialize_state(self, state: "str | list[float] | int") -> "FloatNDArray":
        super()._initialize_state(state)
        self._visualizer.set_state(self._state)
        return self._state

    def x(self, i: "int | list[int]") -> "None":
        super().x(i)
        self._visualizer.append_standalone(XGate(), i)

    def h(self, i: "int | list[int]") -> "None":
        super().h(i)
        self._visualizer.append_standalone(HGate(), i)

    def cx(self, c: "int", t: "int") -> "None":
        super().mcx((c,), t)
        self._visualizer.append_controlled(XGate(), c, t)

    def ccx(self, c1: "int", c2: "int", t: "int") -> "None":
        super().mcx((c1, c2), t)
        self._visualizer.append_controlled(XGate(), (c1, c2), t)

    def mcx(self, c_bits: "Iterable[int]", t: "int") -> "None":
        super().mcx(c_bits, t)
        self._visualizer.append_controlled(XGate(), c_bits, t)

    def barrier(self, qubits: "Iterable[int] | None" = None) -> "None":
        """Adds a barrier in the visualization of the circuit.
        It can help to separate different parts of the circuit.

        Args:
            qubits: qubits to which the barrier is applied
        """
        self._visualizer.append_barrier(qubits)

    def __str__(self) -> "str":
        return str(self._visualizer)
