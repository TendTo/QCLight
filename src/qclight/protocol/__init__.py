"""Quantum protocols take advantage of the peculiarities of quantum mechanics
to guarantee a set of properties in the communication between two agents.

One of the areas where quantum protocols is be able to share a secret key
between two agents in a secure way over an insecure channel.
This task is called quantum key distribution (QKD).

The protocols implemented in this module are `BB84 <https://en.wikipedia.org/wiki/BB84>`_ and
`E91 <https://www.researchgate.net/publication/252207648_Experimental_E91_quantum_key_distribution>`_.
"""
from .protocol import Protocol
from .agent import Agent
from .message import Message
from .verbose_protocol import VerboseProtocol
