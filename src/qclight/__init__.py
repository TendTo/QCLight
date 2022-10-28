"""QCLight is a lightweight Python library able to simulate quantum computing.

The only dependency is NumPy, since the circuit and the operations are expressed
as vectors and matrices, and NumPy allows to improve the performance of this kind of operations.

QCLight is theoretically able to simulate quantum circuits with up to any number of qubits,
but keep in mind that the operations scale exponentially with the number of qubits involved.
"""

from .circuit.circuit import QCLCircuit

# Version of the QCLight package
__version__ = "0.0.2"

# Read URL of the Real Python feed from config file
# _cfg = resources.read_text("reader", "config.toml")
# URL = _cfg["feed"]["url"]
