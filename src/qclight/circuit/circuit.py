"""QCLCircuit class"""
import re
from typing import Any
import numpy as np
from qclight.utils import extract_bits
from qclight.gates import Gate
from qclight.error import BinaryStringError, PositiveValueError, PowerOfTwoLengthError

FloatNDArray = np.ndarray[Any, np.dtype[np.float64]]


class QCLCircuit:
    """Quantum circuit used for a generic computation"""

    def __init__(self, state: "str | list[float] | int") -> "None":
        """QCLCircuit constructor.

        Args:
            state: initial state of the circuit
        """
        self._state: "FloatNDArray"
        self._n: "int"
        self.gates: "list[FloatNDArray]"
        self._result: "FloatNDArray | None"
        self._identity: "FloatNDArray"
        self._initialize_state(state)

    @property
    def n(self) -> "int":
        """Number of qubits in the circuit."""
        return self._n

    @n.setter
    def n(self, n: "int") -> "None":
        self._n = n
        self._identity = self.tp([Gate.I] * n)

    @property
    def state(self) -> "FloatNDArray":
        """Initial state of the circuit."""
        return self._state

    @property
    def result(self) -> "FloatNDArray":
        """Result of the last simulation
        or the initial state if no simulation has been run yet.
        """
        return self._result if self._result is not None else self._state

    def __normalize(self, vector: "FloatNDArray") -> "FloatNDArray":
        """Normalize an array so that the sum of all the elements is 1.

        Args:
            vector: state to be normalized

        Raises:
            ValueError: the current norm of the vector is 0

        Returns:
            normalized vector
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            raise ValueError("Cannot normalize a zero vector")
        if np.isclose(norm, 1):
            return vector
        return vector / norm

    def _initialize_state(self, state: "str | list[float] | int") -> "FloatNDArray":
        """Initializes the state of the circuit.
        The state is initialized so that the probability of measuring state is 100%.
        The circuit is effectively reset, so no gates are applied.

        Args:
            state: set the initial state of the circuit so that
            there is 100% probability of measuring the provided state
        """
        self.gates = []
        self._result = None
        if isinstance(state, str):
            if re.match(r"^[01]+$", state) is None:
                raise BinaryStringError(state)
            self.n = len(state)
            self._state = np.zeros(2**self.n)
            pos = int(state, 2)
            self._state[pos] = 1
        elif isinstance(state, list):
            length = len(state)
            if (length & (length - 1) != 0) or length == 0:
                raise PowerOfTwoLengthError(length)
            self._state = self.__normalize(np.array(state))
            self.n = length.bit_length() - 1
        elif isinstance(state, int):
            if state <= 0:
                raise PositiveValueError(state)
            self._state = np.zeros(2**state)
            self._state[0] = 1
            self.n = state
        return self._state

    def _initialize_circuit(self, state: "str") -> "None":
        """Builds a circuit that output the provided state starting from the all-zero state.

        Args:
            state: state to be outputted
        """
        if not isinstance(state, str) or re.match(r"^[01h]+$", state) is None:
            raise ValueError("state must be a string that verifies the regex ^[01h]+$")
        if len(state) != self.n:
            raise ValueError(f"state must be a string of length n={self.n}")
        self.gates = []
        self._result = None
        self._state = np.zeros(2**self.n)
        self._state[0] = 1
        x_list = [i for i, digit in enumerate(state) if digit == "1"]
        h_list = [i for i, digit in enumerate(state) if digit == "h"]
        self.x(x_list)
        self.h(h_list)

    def expand_gate(
        self, single_gate: "FloatNDArray", positions: "int | list[int]"
    ) -> "FloatNDArray":
        """Expands a single gate so that all the qubits are included.
        All the qubits in the positions specified by position will be affected by the gate,
        while the others will be multiplied by the identity matrix.

        Args:
            single_gate: gate to be expanded
            i: position or list of positions directly affected by the gate

        Returns:
            expanded gate
        """
        expanded_gate = [Gate.I] * self.n
        if isinstance(positions, int):
            positions = [positions]
        if isinstance(positions, list):
            for position in positions:
                expanded_gate[position] = single_gate
        return self.tp(expanded_gate)

    def tp(self, gates: "list[FloatNDArray]") -> "FloatNDArray":
        """Calculates the tensor product between all the gates in the list.

        Args:
            gates: list of gates to be multiplied

        Raises:
            ValueError: the list of gates is empty

        Returns:
            the tensor product of all the gates in the list
        """
        if len(gates) == 0:
            raise ValueError("ql must not be empty")
        v = gates[0]
        for gate in gates[1:]:
            v = np.kron(v, gate)
        return v

    def x(self, i: "int | list[int]") -> "None":
        """Applies a :attr:`~qclight.gates.gates.Gate.X` gate to the qubit in position i.

        | i | X |
        |---|---|
        | 0 | 1 |
        | 1 | 0 |

        .. table:: Truth table of the X gate.

            === ===
             i   X
            === ===
             0   1
             1   0
            === ===

        Args:
            i: position of the qubit to be affected by the gate
        """
        self.gates.append(self.expand_gate(Gate.X, i))

    def h(self, i: "int | list[int]") -> "None":
        """Applies a :attr:`~qclight.gates.gates.Gate.H` gate to the qubit in position i.

        Args:
            i: position of the qubit to be affected by the gate
        """
        self.gates.append(self.expand_gate(Gate.H, i))

    def cx(self, c: "int", t: "int") -> "None":
        """Applies a cx gate controlled by the qubit in position c.
        The qubit in position t will be negated if the control qubit is 1.

        | c | t | CX |
        |:-:|:-:|:--:|
        | 0 | 0 | 0  |
        | 0 | 1 | 1  |
        | 1 | 0 | 1  |
        | 1 | 1 | 0  |

        .. table:: Truth table of the CX gate.

            === === ====
             c   t   CX
            === === ====
             0   0   0
             0   1   1
             1   0   1
             1   1   0
            === === ====

        Args:
            c: position of the qubit controlling the gate
            t: position of the qubit to be affected by the gate
        """
        identity = self._identity.copy()
        c_mask = 1 << self.n - c - 1
        t_mask = 1 << self.n - t - 1
        for i in range(self._state.size):
            if i & c_mask and not i & t_mask:
                swap_idx = i | t_mask
                identity[i], identity[swap_idx] = (
                    identity[swap_idx].copy(),
                    identity[i].copy(),
                )
        self.gates.append(identity)

    def ccx(self, c1: "int", c2: "int", t: "int") -> "None":
        """Applies a ccx gate controlled by both qubits in position c1 and c2.
        The qubit in position t will be negated if both control qubits are 1.

        | c1 | c1 | t | CCX |
        |:--:|:--:|:-:|:---:|
        | 0  | 0  | 0 |  0  |
        | 0  | 1  | 0 |  0  |
        | 1  | 0  | 0 |  0  |
        | 1  | 1  | 0 |  1  |
        | 0  | 0  | 1 |  1  |
        | 0  | 1  | 1 |  1  |
        | 1  | 0  | 1 |  1  |
        | 1  | 1  | 1 |  0  |

        .. table:: Truth table of the CCX gate.

            ==== ==== ==== ====
             c1   c2   t   CCX
            ==== ==== ==== ====
             0    0    0    0
             0    1    0    0
             1    0    0    0
             1    1    0    1
             0    0    1    1
             0    1    1    1
             1    0    1    1
             1    1    1    0
            ==== ==== ==== ====

        Args:
            c1: position of the first qubit controlling the gate
            c2: position of the second qubit controlling the gate
            t: position of the qubit to be affected by the gate
        """
        identity = self._identity.copy()
        c1_mask = 1 << self.n - c1 - 1
        c2_mask = 1 << self.n - c2 - 1
        t_mask = 1 << self.n - t - 1
        for i in range(self._state.size):
            if i & c1_mask and i & c2_mask and not i & t_mask:
                swap_idx = i | t_mask
                identity[i], identity[swap_idx] = (
                    identity[swap_idx].copy(),
                    identity[i].copy(),
                )
        self.gates.append(identity)

    def or_(self, q1: "int", q2: "int", t: "int") -> "None":
        """Applies an OR gate to the qubits in position q1 and q2.
        The result will be stored in the qubit in position t.

        | q1 | q2 | OR |
        |:--:|:--:|:--:|
        | 0  | 0  | 0  |
        | 0  | 1  | 1  |
        | 1  | 0  | 1  |
        | 1  | 1  | 1  |

        .. table:: Truth table of the OR gate.

            ==== ==== ====
             q1   q2   OR
            ==== ==== ====
             0    0    0
             0    1    1
             1    0    1
             1    1    1
            ==== ==== ====
        """
        self.cx(q1, t)
        self.cx(q2, t)
        self.ccx(q1, q2, t)

    def swap(self, i: "int", j: "int") -> "None":
        """Swaps the qubit in position i with the qubit in position j.

        Args:
            i: position of the first qubit to be swapped
            j: position of the second qubit to be swapped
        """
        self.cx(i, j)
        self.cx(j, i)
        self.cx(i, j)

    def run(self) -> "FloatNDArray":
        """Runs the simulator and returns the result.

        Returns:
            results of the computation
        """
        result = self._state
        for gate in self.gates:
            result = np.matmul(result, gate)
        self._result = result
        return self.result

    def counts(
        self, auto_run: "bool" = True, msr_list: "list[int] | None" = None
    ) -> "None":
        """Shows the result of the computation and the probability for each to happen.
        If auto_run is True, the circuit is run before showing the result.
        If an msr_list is provided, the result is shown only for the qubits with that index.

        Args:
            auto_run: whether to run the circuit before showing the result
            msr_list: list of indices of the qubits to be considered
        """
        if auto_run:
            self.run()

        print("RESULTS:")
        # Show the results for all qubits
        if msr_list is None or len(msr_list) == 0:
            for i, digit in enumerate(self.result):
                if digit > 0:
                    print(f"{i:0{self.n}b} - {np.square(digit) * 100:.2f}%")
            return

        # Show the results only considering the state of the qubits in msr_list
        msr: dict[int, np.float16] = {}
        for i, digit in enumerate(self.result):
            idx = extract_bits(i, msr_list)
            prb = np.square(digit)
            if idx in msr:
                msr[idx] += prb
            else:
                msr[idx] = prb
        for i, prb in msr.items():
            if prb > 0:
                print(f"{i:0{len(msr_list)}b} - {prb:.2f}%")

    def measure(
        self, auto_run: "bool" = True, msr_list: "list[int] | None" = None
    ) -> "None":
        """Collapses the qubits and show their value as a classical bit.
        If auto_run is True, the circuit is run before showing the result.
        If an msr_list is provided, the result is shown only for the qubits with that index.

        Args:
            auto_run: whether to run the circuit before showing the result
            msr_list: list of indices of the qubits to be measured
        """
        if msr_list is None:
            msr_list = list(range(self.n))
        if auto_run:
            self.run()
