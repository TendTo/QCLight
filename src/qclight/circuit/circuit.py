import re
from typing import Any
import numpy as np
from qclight.gates import Gate
from qclight.error import BinaryStringError, PositiveValueError, PowerOfTwoLengthError

FloatNDArray = np.ndarray[Any, np.dtype[np.float64]]


class QCLCircuit:
    """Quantum circuit used for computation"""

    def __init__(self, state: str | list[float] | int) -> None:
        """QCLCircuit constructor.

        Args:
            state: initial state of the circuit
        """
        self._state: FloatNDArray
        self._n: int
        self.gates: list[FloatNDArray]
        self._result: FloatNDArray | None
        self._initialize_state(state)

    @property
    def n(self) -> int:
        """Number of qubits in the circuit."""
        return self._n

    @property
    def state(self) -> FloatNDArray:
        """Initial state of the circuit."""
        return self._state

    @property
    def result(self) -> FloatNDArray:
        """Result of the last simulation
        or the initial state if no simulation has been run yet.
        """
        return self._result or self._state

    def __normalize(self, vector: FloatNDArray) -> FloatNDArray:
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

    def _initialize_state(self, state: str | list[float] | int) -> FloatNDArray:
        """Initializes the state of the circuit.
        The state is initialized so that the probability of measuring :param:`state` is 100%.
        The circuit is effectively reset, so no gates are applied.

        Args:
            state: set the initial state of the circuit so that there is 100% probability of getting the provided state
        """
        self.gates = []
        self._result = None
        if isinstance(state, str):
            if re.match(r"^[01]+$", state) is None:
                raise BinaryStringError(state)
            self._n = len(state)
            self._state = np.zeros(2**self._n)
            pos = int(state, 2)
            self._state[pos] = 1
        elif isinstance(state, list):
            length = len(state)
            if (length & (length - 1) != 0) or length == 0:
                raise PowerOfTwoLengthError(length)
            self._state = self.__normalize(np.array(state))
            self._n = length.bit_length() - 1
        elif isinstance(state, int):
            if state <= 0:
                raise PositiveValueError(state)
            self._state = np.zeros(2**state)
            self._state[0] = 1
            self._n = state
        return self._state

    def _initialize_circuit(self, state: str) -> None:
        """Builds a circuit that output the provided state starting from the all-zero state.

        Args:
            state: state to be outputted
        """
        if not isinstance(state, str) or re.match(r"^[01h]+$", state) is None:
            raise ValueError("state must be a string that verifies the regex ^[01h]+$")
        self.gates = []
        self._result = None
        self._state = np.zeros(2**self._n)
        self._state[0] = 1
        self._n = len(state)
        xList = [i for i, digit in enumerate(state) if digit == "1"]
        hList = [i for i, digit in enumerate(state) if digit == "h"]
        self.x(xList)
        self.h(hList)

    def expand_gate(
        self, single_gate: FloatNDArray, positions: int | list[int]
    ) -> FloatNDArray:
        """Expands a single gate so that all the qubits are included.
        All the qubits in the positions specified by {@link positions} will be affected by the gate,
        the others will be multiplied by the identity matrix.

        Args:
            single_gate: gate to be expanded
            i: position or list of positions directly affected by the gate

        Returns:
            expanded gate
        """
        expanded_gate = [Gate.I] * self._n
        if isinstance(positions, int):
            positions = [positions]
        if isinstance(positions, list):
            for position in positions:
                expanded_gate[position] = single_gate
        return self.tp(expanded_gate)

    def tp(self, gates: list[FloatNDArray]) -> FloatNDArray:
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

    def x(self, i: int | list[int]) -> None:
        """Applies a :property:`Gate.X` gate to the qubit in position :param:`i`.

        Args:
            i: position of the qubit to be affected by the gate
        """
        self.gates.append(self.expand_gate(Gate.X, i))

    def h(self, i: int | list[int]) -> None:
        """Applies a :property:`Gate.H` gate to the qubit in position :param:`i`.

        Args:
            i: position of the qubit to be affected by the gate
        """
        self.gates.append(self.expand_gate(Gate.H, i))

    def run(self) -> FloatNDArray | None:
        """Runs the simulator and returns the result.

        Returns:
            results of the computation
        """
        result = self._state
        for gate in self.gates:
            result = np.matmul(result, gate)
        self._result = result
        return self._result

    def print_results(self, auto_run: bool = True):
        """Shows the result of the computation and the probability for each to happen.
        If auto_run is True, the circuit is run before showing the result.

        Args:
            auto_run: whether to run the circuit before showing the result
        """
        if auto_run:
            self.run()

        print("RESULTS:")
        format_str = f"{{:0>{self._n}b}}"
        for i, digit in enumerate(self.result):
            if digit > 0:
                print(
                    f"{format_str.format(i)} - {np.around(digit**2, decimals=2) * 100}%"
                )

    def measure(
        self, auto_run: bool = True, range: tuple[int, int] | None = None
    ) -> None:
        """Collapses the qubits and show their value as a classical bit.
        If auto_run is True, the circuit is run before showing the result.
        If a range is provided, the result is shown only for the qubits in that range.

        Args:
            auto_run: whether to run the circuit before showing the result
            range: range of qubits to measure and show
        """
        if auto_run:
            self.run()

    def __repr__(self) -> str:
        return "QCLCircuit"
