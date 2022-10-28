"""BellCircuit class."""
from .circuit import QCLCircuit


class BellCircuit(QCLCircuit):
    """Bell states are the four states that can be created when two qubits are maximally entangled.
    In this state, the behavior of one qubit affects the other one, and vice versa.

    .. math::

        \\begin{align}
        \\ket{\\Phi^+} = \\frac{\\ket{00} + \\ket{11}}{\\sqrt{2}} \\\\
        \\ket{\\Phi^-} = \\frac{\\ket{00} - \\ket{11}}{\\sqrt{2}} \\\\
        \\ket{\\Psi^+} = \\frac{\\ket{01} + \\ket{10}}{\\sqrt{2}} \\\\
        \\ket{\\Psi^-} = \\frac{\\ket{01} - \\ket{10}}{\\sqrt{2}}
        \\end{align}
    """

    def correlate(self, q1: "int", q2: "int") -> "None":
        """Correlates the two qubits provided.
        The bell state is created by

        - applying a :class:`~qclight.gates.gate.h_gate.HGate` gate to the first qubit
        - applying a :attr:`~qclight.circuit.circuit.QCLCircuit.cx` gate between the two qubits

        Args:
            q1: first qubit to correlate
            q2: second qubit to correlate
        """
        self.h(q1)
        self.cx(q1, q2)
