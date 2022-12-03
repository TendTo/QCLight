from .protocol import Protocol
from .agent import Agent


class E91(Protocol):
    """`E91 <https://www.researchgate.net/publication/252207648_Experimental_E91_quantum_key_distribution>`_ protocol.
    Created by `Artur Ekert <https://en.wikipedia.org/wiki/Artur_Ekert>`_ in 1991.

    .. uml::

    !include https://raw.githubusercontent.com/ptrkcsk/one-dark-plantuml-theme/v1.0.0/theme.puml

    participant Alice as a
    participant Bob as b

    note over a,b: both Alice and bob receive n pairs of entangled qubits
    note over a
        Alice chooses a random sequence of n bases from the set {A1, A2, A3}
        and measures the qubits with the corresponding base
    end note
    note over b
        Bob chooses a random sequence of n bases from the set {B1, B2, B3}
        and measures the qubits with the corresponding base
    end note
    a -> b: sequence of bases Alice chose
    b -> a: sequence of bases Bob chose
    note over a,b
        Alice and Bob assemble a key from the qubits measured with either
        a (A1, B1) or a (A3, B3) bases pair
    end note
    note over a,b
        The qubits measured with either (A1, B3), (A1, B2), (A2, B3) or (A2, B2) bases pair
        are discarded used to check for CHSH inequality violation
    end note
    """

    def __init__(self, attack: "bool" = False) -> "None":
        super().__init__()
        self.attack = attack

    def _setup(self) -> "None":
        """Create the agents that will run the protocol."""
        alice = Agent("Alice")
        alice.add_event("start", lambda p: p.send_message("Bob", "bases"))
        self.add_agent(alice)
