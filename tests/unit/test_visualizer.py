# pylint: disable=missing-function-docstring,too-few-public-methods,redefined-outer-name,protected-access
"""Test visualizer package."""
import pytest
import numpy as np
from qclight.gate import XGate
from qclight.visualizer import Connector, CircuitVisualizer


@pytest.fixture(scope="function")
def visualizer():
    return CircuitVisualizer(5)


@pytest.fixture(scope="function")
def initialized_visualizer():
    visualizer = CircuitVisualizer(5)
    e = Connector.empty()
    b = Connector.barrier()
    visualizer._qubits = [
        [Connector.qubit(0), b, e],
        [Connector.qubit(1), b, e],
        [Connector.qubit(2), b, b],
        [Connector.qubit(3), e, e],
        [Connector.qubit(4), e, e],
    ]
    return visualizer


class TestVisualizer:
    """Tests the visualizer package."""

    class TestCircuitVisualizer:
        """Tests the CircuitVisualizer class"""

        def test_constructor(self):
            visualizer = CircuitVisualizer(3)
            assert visualizer._n == 3
            assert len(visualizer._qubits) == 3
            assert visualizer._qubits == [
                [Connector.qubit(0)],
                [Connector.qubit(1)],
                [Connector.qubit(2)],
            ]

        def test_set_state(self, visualizer: CircuitVisualizer):
            visualizer.set_state(np.array([0, 0, 1, 0]))
            assert visualizer._n == 2
            assert len(visualizer._qubits) == 2
            assert visualizer._qubits == [
                [Connector.qubit(0)],
                [Connector.qubit(1, initial_state=1)],
            ]

        def test_append_barrier_all(self, visualizer: CircuitVisualizer):
            visualizer.append_barrier()
            for qubit in visualizer._qubits:
                assert qubit[-1] == Connector.barrier()

        def test_append_barrier_qubits(self, visualizer: CircuitVisualizer):
            visualizer.append_barrier(qubits=[0, 2])
            for i, qubit in enumerate(visualizer._qubits):
                if i in [0, 2]:
                    assert qubit[-1] == Connector.barrier()
                else:
                    assert qubit[-1] == Connector.empty()

        def test_append_standalone_single(self, visualizer: CircuitVisualizer):
            visualizer.append_standalone(XGate(), 1)
            for i, qubit in enumerate(visualizer._qubits):
                if i == 1:
                    assert qubit[-1] == Connector.from_gate(XGate())
                else:
                    assert qubit[-1] == Connector.empty()

        def test_append_standalone_multiple(self, visualizer: CircuitVisualizer):
            visualizer.append_standalone(XGate(), [2, 3])
            for i, qubit in enumerate(visualizer._qubits):
                if i in [2, 3]:
                    assert qubit[-1] == Connector.from_gate(XGate())
                else:
                    assert qubit[-1] == Connector.empty()

        def test_append_controlled_single(self, visualizer: CircuitVisualizer):
            visualizer.append_controlled(XGate(), 4, 1)
            for i, qubit in enumerate(visualizer._qubits):
                if i == 4:
                    assert qubit[-1] == Connector.control()
                elif i == 1:
                    assert qubit[-1] == Connector.from_gate(XGate())
                elif i in range(1, 4):
                    assert qubit[-1] == Connector.vertical()
                else:
                    assert qubit[-1] == Connector.empty()

        def test_append_controlled_multiple(self, visualizer: CircuitVisualizer):
            visualizer.append_controlled(XGate(), [2, 3], 0)
            for i, qubit in enumerate(visualizer._qubits):
                if i in [2, 3]:
                    assert qubit[-1] == Connector.control()
                elif i == 0:
                    assert qubit[-1] == Connector.from_gate(XGate())
                elif i in range(0, 3):
                    assert qubit[-1] == Connector.vertical()
                else:
                    assert qubit[-1] == Connector.empty()

        def test_first_available_position_single_none(
            self, initialized_visualizer: CircuitVisualizer
        ):
            res = initialized_visualizer._first_available_position(2)
            assert res == -1

        def test_first_available_position_single_one_before(
            self, initialized_visualizer: CircuitVisualizer
        ):
            res = initialized_visualizer._first_available_position(0)
            assert res == 2

        def test_first_available_position_single_two_before(
            self, initialized_visualizer: CircuitVisualizer
        ):
            res = initialized_visualizer._first_available_position(4)
            assert res == 1

        def test_first_available_position_multiple_none(
            self, initialized_visualizer: CircuitVisualizer
        ):
            res = initialized_visualizer._first_available_position([1, 2, 3])
            assert res == -1

        def test_first_available_position_multiple_one_before(
            self, initialized_visualizer: CircuitVisualizer
        ):
            res = initialized_visualizer._first_available_position([0, 1])
            assert res == 2

        def test_first_available_position_multiple_two_before(
            self, initialized_visualizer: CircuitVisualizer
        ):
            res = initialized_visualizer._first_available_position([3, 4])
            assert res == 1
