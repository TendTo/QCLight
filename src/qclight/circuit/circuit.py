"""QCLCircuit class"""
import re
from typing import Iterable
import numpy as np
import numpy.typing as npt
from qclight.utils import extract_bits, range_fixed_bits_switch
from qclight.gate import HGate, XGate, IGate
from qclight.error import BinaryStringError, PositiveValueError, PowerOfTwoLengthError

FloatNDArray = npt.NDArray[np.float64]


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
        self._identity = IGate().matrix_of_size(n)

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

    def initialize_circuit(self, state: "str") -> "None":
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

    def x(self, i: "int | list[int]") -> "None":
        """Applies a :class:`~qclight.gate.x_gate.XGate` gate to the qubit in position i.

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
        self.gates.append(XGate().matrix_of_size(self.n, i))

    def h(self, i: "int | list[int]") -> "None":
        """Applies a :class:`~qclight.gate.h_gate.HGate` gate to the qubit in position i.

        Args:
            i: position of the qubit to be affected by the gate
        """
        self.gates.append(HGate().matrix_of_size(self.n, i))

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
        self.mcx((c,), t)

    def ccx(self, c1: "int", c2: "int", t: "int") -> "None":
        """Applies a ccx gate controlled by both qubits in position c1 and c2.
        The qubit in position t will be negated if both control qubits are 1.

        | c1 | c2 | t | CCX |
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
        self.mcx((c1, c2), t)

    def mcx(self, c_bits: "Iterable[int]", t: "int") -> "None":
        """Applies a mcx gate controlled by all the qubits in position c_bits.
        The qubit in position t will be negated if all control qubits are 1.

        .. math::

            mcx(c_1, c_2, ..., c_n, t) = \\begin{cases}
                \\lnot t & \\text{if } c_1 \\land c_2 \\land \\dots \\land c_n \\\\
                t & \\text{otherwise} \\\\
            \\end{cases}

        Args:
            c_bits: positions of the qubits controlling the gate
            t: position of the qubit to be affected by the gate
        """
        identity = self._identity.copy()
        for idx, swap_idx in range_fixed_bits_switch(self.n, set(c_bits), t):
            identity[idx], identity[swap_idx] = (
                identity[swap_idx].copy(),
                identity[idx].copy(),
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
        msr: "dict[int, np.float16]" = {}
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
