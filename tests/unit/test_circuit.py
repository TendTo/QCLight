# pylint: disable=missing-function-docstring,too-few-public-methods,redefined-outer-name,protected-access
"""Test circuit package."""
import pytest
from pytest_mock import MockerFixture
import numpy as np
from qclight.error import BinaryStringError, PowerOfTwoLengthError, PositiveValueError
from qclight.gate import XGate, HGate
from qclight.circuit import (
    QCLCircuit,
    HalfAdderCircuit,
    BellCircuit,
    RandomCircuit,
    BooleanInnerProductCircuit,
    QCLVisualCircuit,
)


@pytest.fixture(scope="function")
def circuit() -> QCLCircuit:
    return QCLCircuit(3)


@pytest.fixture(scope="function")
def visual_circuit(mocker: MockerFixture) -> QCLVisualCircuit:
    circuit = QCLVisualCircuit(3)
    circuit._visualizer = mocker.Mock(wraps=circuit._visualizer)
    return circuit


class TestCircuit:
    """Tests the circuit package."""

    class TestQCLCircuit:
        """Tests the QCLCircuit class."""

        def test_construct_string_all_zero(self):
            circuit = QCLCircuit("000")
            assert circuit.n == 3
            assert np.array_equal(circuit.state, [1, 0, 0, 0, 0, 0, 0, 0])

        def test_construct_string_with_ones(self):
            circuit = QCLCircuit("0110")
            assert circuit.n == 4
            assert np.array_equal(
                circuit.state, [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            )

        def test_construct_string_invalid_char(self):
            with pytest.raises(BinaryStringError, match=r"received 'non valid string'"):
                QCLCircuit("non valid string")

        def test_construct_array_deterministic(self):
            circuit = QCLCircuit([0, 1, 0, 0])
            assert circuit.n == 2
            assert np.array_equal(circuit.state, [0, 1, 0, 0])

        def test_construct_array_non_deterministic(self):
            circuit = QCLCircuit([1, 1, 1, 1, 0, 0, 0, 0])
            assert circuit.n == 3
            assert np.array_equal(circuit.state, [0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0])

        def test_construct_array_invalid_length(self):
            with pytest.raises(PowerOfTwoLengthError, match=r"received '3'"):
                QCLCircuit([0, 1, 0])

        def test_construct_int(self):
            circuit = QCLCircuit(3)
            assert circuit.n == 3
            assert np.array_equal(circuit.state, [1, 0, 0, 0, 0, 0, 0, 0])

        def test_construct_int_negative(self):
            with pytest.raises(PositiveValueError, match=r"received '-1'"):
                QCLCircuit(-1)

        def test_construct_int_zero(self):
            with pytest.raises(PositiveValueError, match=r"received '0'"):
                QCLCircuit(0)

        def test_x_gate_int(self, circuit: QCLCircuit):
            circuit.x(1)
            assert np.array_equal(circuit.run(), [0, 0, 1, 0, 0, 0, 0, 0])

        def test_x_gate_list(self, circuit: QCLCircuit):
            circuit.x([0, 2])
            assert np.array_equal(circuit.run(), [0, 0, 0, 0, 0, 1, 0, 0])

        def test_h_gate_int(self, circuit: QCLCircuit):
            circuit.h(1)
            assert np.allclose(
                circuit.run(), [0.70710678, 0, 0.70710678, 0, 0, 0, 0, 0]
            )

        def test_h_gate_list(self, circuit: QCLCircuit):
            circuit.h([0, 2])
            assert np.allclose(circuit.run(), [0.5, 0.5, 0, 0, 0.5, 0.5, 0, 0])

        def test_cx_gate_c_zero(self, circuit: QCLCircuit):
            circuit.cx(0, 2)
            assert np.allclose(circuit.run(), [1, 0, 0, 0, 0, 0, 0, 0])

        def test_cx_gate_c_one(self, circuit: QCLCircuit):
            circuit.x(0)
            circuit.cx(0, 1)
            assert np.allclose(circuit.run(), [0, 0, 0, 0, 0, 0, 1, 0])

        def test_ccx_gate_c_zero(self, circuit: QCLCircuit):
            circuit.ccx(0, 1, 2)
            assert np.allclose(circuit.run(), [1, 0, 0, 0, 0, 0, 0, 0])

        def test_ccx_gate_c1_one(self, circuit: QCLCircuit):
            circuit.x(0)
            circuit.ccx(0, 1, 2)
            assert np.allclose(circuit.run(), [0, 0, 0, 0, 1, 0, 0, 0])

        def test_ccx_gate_c2_one(self, circuit: QCLCircuit):
            circuit.x(1)
            circuit.ccx(0, 1, 2)
            assert np.allclose(circuit.run(), [0, 0, 1, 0, 0, 0, 0, 0])

        def test_ccx_gate_c1_c2_one(self, circuit: QCLCircuit):
            circuit.x(0)
            circuit.x(1)
            circuit.ccx(0, 1, 2)
            assert np.allclose(circuit.run(), [0, 0, 0, 0, 0, 0, 0, 1])

        def test_mcx_gate_three_c_false(self):
            circuit = QCLCircuit(4)
            circuit.mcx([0, 1, 2], 3)
            assert np.allclose(
                circuit.run(), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            )

        def test_mcx_gate_three_c_true(self):
            circuit = QCLCircuit(4)
            circuit.x(0)
            circuit.x(1)
            circuit.x(2)
            circuit.mcx([0, 1, 2], 3)
            assert np.allclose(
                circuit.run(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            )

        def test_swap_gate_equal(self, circuit: QCLCircuit):
            circuit.swap(0, 1)
            assert np.allclose(circuit.run(), [1, 0, 0, 0, 0, 0, 0, 0])

        def test_swap_gate_different(self, circuit: QCLCircuit):
            circuit.x(0)
            circuit.swap(0, 2)
            assert np.allclose(circuit.run(), [0, 1, 0, 0, 0, 0, 0, 0])

        def test_or_gate_zero_zero(self, circuit: QCLCircuit):
            circuit.or_(0, 1, 2)
            assert np.allclose(circuit.run(), [1, 0, 0, 0, 0, 0, 0, 0])

        def test_or_gate_one_zero(self, circuit: QCLCircuit):
            circuit.x(0)
            circuit.or_(0, 1, 2)
            assert np.allclose(circuit.run(), [0, 0, 0, 0, 0, 1, 0, 0])

        def test_or_gate_zero_one(self, circuit: QCLCircuit):
            circuit.x(1)
            circuit.or_(0, 1, 2)
            assert np.allclose(circuit.run(), [0, 0, 0, 1, 0, 0, 0, 0])

        def test_or_gate_one_one(self, circuit: QCLCircuit):
            circuit.x(0)
            circuit.x(1)
            circuit.or_(0, 1, 2)
            assert np.allclose(circuit.run(), [0, 0, 0, 0, 0, 0, 0, 1])

    class TestHalfAdder:
        """Tests the HalfAdderCircuit class."""

        def test_constructor_zero_zero(self):
            half_adder = HalfAdderCircuit(0, 0)
            assert np.array_equal(half_adder.sum(), 0)

        def test_constructor_one_zero(self):
            half_adder = HalfAdderCircuit(1, 0)
            assert np.array_equal(half_adder.sum(), 1)

        def test_constructor_zero_one(self):
            half_adder = HalfAdderCircuit(0, 1)
            assert np.array_equal(half_adder.sum(), 1)

        def test_constructor_one_one(self):
            half_adder = HalfAdderCircuit(1, 1)
            assert np.array_equal(half_adder.sum(), 0b10)

    class TestBellCircuit:
        """Tests the BellCircuit class."""

        def test_correlation_zero_zero(self):
            bell = BellCircuit(2)
            bell.correlate(0, 1)
            assert np.allclose(bell.run(), [0.70710678, 0, 0, 0.70710678])

        def test_correlation_one_zero(self):
            bell = BellCircuit(2)
            bell.x(0)
            bell.correlate(0, 1)
            assert np.allclose(bell.run(), [0.70710678, 0, 0, -0.70710678])

        def test_correlation_zero_one(self):
            bell = BellCircuit(2)
            bell.x(1)
            bell.correlate(0, 1)
            assert np.allclose(bell.run(), [0, 0.70710678, 0.70710678, 0])

        def test_correlation_one_one(self):
            bell = BellCircuit(2)
            bell.x(0)
            bell.x(1)
            bell.correlate(0, 1)
            assert np.allclose(bell.run(), [0, 0.70710678, -0.70710678, 0])

    class TestRandomCircuit:
        """Tests the RandomCircuit class."""

        def test_run_one(self):
            random_circuit = RandomCircuit(1)
            random_circuit.run()
            assert random_circuit.n == 1
            assert np.allclose(random_circuit.run(), [0.70710678, 0.70710678])

        def test_run_two(self):
            random_circuit = RandomCircuit(2)
            random_circuit.run()
            assert random_circuit.n == 2
            assert np.allclose(random_circuit.run(), [0.5, 0.5, 0.5, 0.5])

        def test_run_three(self):
            random_circuit = RandomCircuit(3)
            random_circuit.run()
            assert random_circuit.n == 3
            assert np.allclose(
                random_circuit.run(),
                [
                    0.35355339,
                    0.35355339,
                    0.35355339,
                    0.35355339,
                    0.35355339,
                    0.35355339,
                    0.35355339,
                    0.35355339,
                ],
            )

    class TestBooleanInnerProductCircuit:
        """Tests the BooleanInnerProductCircuit class."""

        def test_product_same_length_true(self):
            a = 0b101
            b = 0b110
            inner_product = BooleanInnerProductCircuit(a, b)
            assert inner_product.inner_product() is True

        def test_product_same_length_false(self):
            a = 0b101
            b = 0b111
            inner_product = BooleanInnerProductCircuit(a, b)
            assert inner_product.inner_product() is False

        def test_product_different_length_true(self):
            a = 0b1101
            b = 0b110
            inner_product = BooleanInnerProductCircuit(a, b)
            assert inner_product.inner_product() is True

        def test_product_different_length_false(self):
            a = 0b101
            b = 0b1111
            inner_product = BooleanInnerProductCircuit(a, b)
            assert inner_product.inner_product() is False

    class TestQCLVisualCircuit:
        """Tests the QCLVisualCircuit class"""

        def test_constructor(self):
            circuit = QCLVisualCircuit(3)
            assert circuit.n == 3
            assert circuit._visualizer is not None

        def test_set_n(self):
            circuit = QCLVisualCircuit(3)
            assert circuit.n == 3
            assert circuit._visualizer._n == 3
            assert len(circuit._visualizer._qubits) == 3
            circuit.n = 5
            assert circuit.n == 5
            assert circuit._visualizer._n == 5
            assert len(circuit._visualizer._qubits) == 5


        def test_x_gate_single(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.x(0)
            visual_circuit._visualizer.append_standalone.assert_called_once_with(
                XGate(), 0
            )

        def test_x_gate_multiple(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.x([0, 1])
            visual_circuit._visualizer.append_standalone.assert_called_once_with(
                XGate(), [0, 1]
            )

        def test_h_gate_single(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.h(0)
            visual_circuit._visualizer.append_standalone.assert_called_once_with(
                HGate(), 0
            )

        def test_h_gate_multiple(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.h([0, 1])
            visual_circuit._visualizer.append_standalone.assert_called_once_with(
                HGate(), [0, 1]
            )

        def test_cx_gate(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.cx(0, 1)
            visual_circuit._visualizer.append_controlled.assert_called_once_with(
                XGate(), 0, 1
            )

        def test_ccx_gate(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.ccx(0, 1, 2)
            visual_circuit._visualizer.append_controlled.assert_called_once_with(
                XGate(), (0, 1), 2
            )

        def test_mcx_gate(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.mcx((0, 1), 2)
            visual_circuit._visualizer.append_controlled.assert_called_once_with(
                XGate(), (0, 1), 2
            )

        def test_barrier_all(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.barrier()
            visual_circuit._visualizer.append_barrier.assert_called_once_with(None)

        def test_barrier_qubits(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.barrier([0, 1])
            visual_circuit._visualizer.append_barrier.assert_called_once_with([0, 1])

        def test_barrier_qubits_invalid(self, visual_circuit: QCLVisualCircuit):
            visual_circuit.barrier([20])
            visual_circuit._visualizer.append_barrier.assert_called_once_with([20])
