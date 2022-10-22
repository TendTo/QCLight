"""Gate class"""
import numpy as np


class Gate:
    """Gates are the basic building blocks of quantum circuits.
    They are used to manipulate the state of a quantum system and compute functions.
    """

    X = np.array([[0, 1], [1, 0]])
    Z = np.array([[1, 0], [0, -1]])
    H = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
    I = np.array([[1, 0], [0, 1]])
