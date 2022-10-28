# pylint: disable=missing-function-docstring,too-few-public-methods,redefined-outer-name,invalid-name
"""Test gate package."""
import pytest

import numpy as np
from qclight.gate import HGate, XGate, ZGate, IGate
from qclight.gate.gate import Gate


@pytest.fixture(scope="function")
def base_gate() -> "Gate":
    """Returns a gate."""
    return Gate()


class TestGate:
    """Tests the gate package."""

    def test_abstract_base_gate(self, base_gate: Gate):
        with pytest.raises(NotImplementedError):
            base_gate.matrix  # pylint: disable=pointless-statement

    def test_tp(self, base_gate: Gate):
        gates = [np.array([[0, 1], [1, 0]])] * 2
        tp_gates = base_gate.tp(gates)
        assert tp_gates.shape == (4, 4)
        assert np.array_equal(
            tp_gates,
            np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]),
        )

    def test_I_gate(self):
        gate = IGate()
        assert gate.matrix.shape == (2, 2)
        assert np.array_equal(gate.matrix, np.eye(2))

    def test_X_gate(self):
        gate = XGate()
        assert gate.matrix.shape == (2, 2)
        assert np.array_equal(gate.matrix, np.array([[0, 1], [1, 0]]))

    def test_Z_gate(self):
        gate = ZGate()
        assert gate.matrix.shape == (2, 2)
        assert np.array_equal(gate.matrix, np.array([[1, 0], [0, -1]]))

    def test_H_gate(self):
        gate = HGate()
        assert gate.matrix.shape == (2, 2)
        assert np.array_equal(gate.matrix, np.array([[1, 1], [1, -1]]) / np.sqrt(2))
