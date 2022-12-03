"""BB84 class."""
from .protocol import Protocol
from .agent import Agent


class BB84(Protocol):
    """BB84 protocol.

    .. uml::

        !include https://raw.githubusercontent.com/ptrkcsk/one-dark-plantuml-theme/v1.0.0/theme.puml

        participant Alice as a
        participant Bob as b

        note over a
            prepares a random sequence of
            n bits (0, 1) and n bases (Z, X)
        end note
        a -> b: qubits encoded in the random bases
        note over b: prepares a random sequence of n bases (Z, X)
        note over b: measures the qubits in the random bases he chose
        b -> a: sequence of bases chosen by Bob
        a -> b: sequence of bases Alice encoded in the qubits with
        note over a,b
            discards the qubits measured in a different basis
            than the one encoded in
        end note
        note over a,b
            choose the same random subset of the remaining
            qubits (can be communicated over an insicure channel)
        end note
        a -> b: random subset of qubits
        b -> a: random subset of qubits
        alt the subsets are equal
            note over a,b: the key is secure
        else
            note over a,b: the key is compromised
        end
    """

    def __init__(self, intercept: "bool") -> "None":
        super().__init__()
        self.intercept = intercept

    def _setup(self) -> "None":
        """Create the agents that will run the protocol."""
        alice = Agent("Alice")
        self.add_agent(alice)

    def start(self) -> "None":
        self._setup()
        return super().start()
