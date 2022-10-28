"""Circuits allow to simulate the computation on a quantum computer.

The circuit is a sequence of quantum gates that are applied to the qubits.
Since the simulator runs on a classical computer, the gates are applied using
matrix multiplication, and the state of all qubits is represented as a vector.

When the qubits are measured, the state of the qubits collapses using a random
number generator that follows the probability distribution of the state vector.
"""
from .circuit import QCLCircuit
from .bell import BellCircuit
from .boolean_inner_product import BooleanInnerProductCircuit
from .random import RandomCircuit
from .half_adder import HalfAdderCircuit
