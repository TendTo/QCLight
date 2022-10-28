"""Connector class"""
from qclight.gate import Gate


class Connector:
    """Connector that will be used to represent a block of the quantum circuit.
    It can be a qubit, a gate, a barrier, a control or a vertical line.
    """

    def __init__(self, content: str):
        self._content = content

    @classmethod
    def from_gate(cls, gate: Gate) -> "Connector":
        """Creates a connector from a gate.

        Args:
            gate: gate to create the connector from

        Returns:
            new connector
        """
        return cls(f"|{gate}|")

    @classmethod
    def empty(cls) -> "Connector":
        """Creates an empty connector.

        Returns:
            new connector
        """
        return cls("───")

    @classmethod
    def vertical(cls) -> "Connector":
        """Creates a vertical connector.
        Used in controlled gates.

        Returns:
            new connector
        """
        return cls("─│─")

    @classmethod
    def control(cls) -> "Connector":
        """Creates a control connector.
        Used in controlled gates, to indicate the control qubits.

        Returns:
            new connector
        """
        return cls("─■─")

    @classmethod
    def barrier(cls) -> "Connector":
        """Creates a barrier connector.
        Used to separate different parts of the circuit.

        Returns:
            new connector
        """
        return cls("─░─")

    @classmethod
    def qubit(
        cls, idx: "int", label: "str" = "q", initial_state: "int | str" = 0
    ) -> "Connector":
        """Creates a qubit connector.
        It indicates the name and index of the qubit, as well as its initial state.

        Args:
            idx: index of the qubit
            label: label of the qubit
            initial_state: initial state of the qubit

        Returns:
            new connector
        """
        return cls(f"{label}_{idx} |{initial_state}>")

    def is_empty(self) -> "bool":
        """Checks if the connector is an empty connector.

        Returns:
            whether the connector is empty
        """
        return self._content == "───"

    def __eq__(self, other: object) -> "bool":
        return (
            isinstance(other, self.__class__)
            and self._content == other._content  # type: ignore
        )

    def __str__(self) -> "str":
        return self._content
