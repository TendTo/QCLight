"""CircuitVisualizer class"""
from typing import Iterable
import numpy as np
import numpy.typing as npt
from qclight.gate import Gate
from .connector import Connector


class CircuitVisualizer:
    """Utility class used to visualize quantum circuits using connectors."""

    def __init__(self, n_qubits: "int"):
        self._n = n_qubits
        self._qubits: "list[list[Connector]]" = []
        for i in range(n_qubits):
            self._qubits.append([Connector.qubit(i)])

    def append_standalone(self, gate: "Gate", qubits: "int | Iterable[int]"):
        """Appends a standalone gate to the provided qubit in the first available position.
        If the qubits are more than one, the gate will be applied to all of them
        at the same position.

        Args:
            gate: gate to apply
            qubits: qubits to apply the gate to
        """
        if isinstance(qubits, int):
            qubits = [qubits]
        pos = self._first_available_position(qubits)
        if pos == -1:
            for i in range(self._n):
                if i in qubits:
                    self._qubits[i].append(Connector.from_gate(gate))
                else:
                    self._qubits[i].append(Connector.empty())
        else:
            for q in qubits:
                self._qubits[q][pos] = Connector.from_gate(gate)

    def append_barrier(self, qubits: "Iterable[int] | None" = None):
        """Appends a barrier to the circuit.
        If no qubits are specified, it will be added to all of them.
        It separates the circuit in different parts.

        Args:
            qubits: qubits to add the barrier to
        """
        for i in range(self._n):
            if qubits is None:
                self._qubits[i].append(Connector.barrier())
            elif i in qubits:
                self._qubits[i].append(Connector.barrier())
            else:
                self._qubits[i].append(Connector.empty())

    def append_controlled(
        self, gate: "Gate", control: "int | Iterable[int]", target: "int"
    ):
        """Appends a gate controlled by the control qubits and targeting the target qubit.
        All the qubits between the control and the target will be marked with vertical lines.

        Args:
            gate: gate to apply
            control: control qubits
            target: target qubit
        """
        if isinstance(control, int):
            control = [control]
        q_min = min([*control, target])
        q_max = max([*control, target])
        pos = self._first_available_position(range(q_min, q_max + 1))
        if pos == -1:
            for qubit in range(self._n):
                if qubit == target:
                    self._qubits[qubit].append(Connector.from_gate(gate))
                elif qubit in control:
                    self._qubits[qubit].append(Connector.control())
                elif q_min < qubit < q_max:
                    self._qubits[qubit].append(Connector.vertical())
                else:
                    self._qubits[qubit].append(Connector.empty())
        else:
            for qubit in range(q_min, q_max + 1):
                if qubit == target:
                    self._qubits[qubit][pos] = Connector.from_gate(gate)
                elif qubit in control:
                    self._qubits[qubit][pos] = Connector.control()
                elif q_min < qubit < q_max:
                    self._qubits[qubit][pos] = Connector.vertical()

    def set_state(self, state: "npt.NDArray[np.float64]"):
        """Sets the initial state of the circuit.

        Args:
            state: initial state of the circuit
        """
        self._n = int(np.log2(len(state)))
        state_str = f"{np.where(state == 1)[0][0]:0{self._n}b}"[::-1]

        self._qubits = []
        for i, qubit in enumerate(state_str):
            self._qubits.append([Connector.qubit(i, initial_state=qubit)])

    def _first_available_position(self, qubits: "int | Iterable[int]") -> "int":
        """Calculates the first available position for the provided qubits.
        It shows the last position from the end where all the qubits specified are empty.
        It stops as soon as it finds a qubit among the ones indicated that is not empty.
        If no valid position was found, it returns -1.

        Args:
            qubits: qubits that must be empty

        Returns:
            last position from the end where all the qubits specified are empty or -1
        """
        if isinstance(qubits, int):
            qubits = [qubits]
        min_idx = []
        for i in range(len(self._qubits[0]) - 1, -1, -1):
            for qubit in qubits:
                if not self._qubits[qubit][i].is_empty():
                    break
            else:
                min_idx.append(i)
                continue
            break
        return min(min_idx) if len(min_idx) > 0 else -1

    def __str__(self):
        return "\n".join(["".join([str(c) for c in q]) for q in self._qubits])
