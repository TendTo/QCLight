"""Init"""

from importlib import resources
from .circuit.circuit import QCLCircuit

# Version of the QCLight package
__version__ = "0.0.1"

# Read URL of the Real Python feed from config file
# _cfg = resources.read_text("reader", "config.toml")
# URL = _cfg["feed"]["url"]
