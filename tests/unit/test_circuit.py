# pylint: disable=missing-function-docstring,too-few-public-methods,redefined-outer-name
import pytest
import numpy as np
from qclight.error import BinaryStringError, PowerOfTwoLengthError, PositiveValueError
from qclight.circuit import QCLCircuit, SumCircuit


@pytest.fixture(scope="function")
def circuit():
    return QCLCircuit(3)


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

        def test_tp(self, circuit: QCLCircuit):
            gates = [np.array([[0, 1], [1, 0]])] * 2
            tp_gates = circuit.tp(gates)
            assert tp_gates.shape == (4, 4)
            assert np.array_equal(
                tp_gates,
                np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]),
            )

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

        def test_swap_gate_equal(self, circuit: QCLCircuit):
            circuit.swap(0, 1)
            assert np.allclose(circuit.run(), [1, 0, 0, 0, 0, 0, 0, 0])

        def test_swap_gate_different(self, circuit: QCLCircuit):
            circuit.x(0)
            circuit.swap(0, 2)
            assert np.allclose(circuit.run(), [0, 1, 0, 0, 0, 0, 0, 0])

    class TestSumCircuit:
        def test_constructor_same_length(self):
            a, b = 0b101, 0b110
            sum_c = SumCircuit(a, b)
            assert sum_c.n == 3 + 3 + 4
            assert sum_c.sum() == a + b

        def test_constructor_different_length(self):
            a, b = 0b101, 0b1101
            sum_c = SumCircuit(a, b)
            assert sum_c.n == 3 + 4 + 5
            assert sum_c.sum() == a + b

        def test_constructor_with_zero(self):
            a, b = 0b0, 0b1111
            sum_c = SumCircuit(a, b)
            assert sum_c.n == 1 + 4 + 5
            assert sum_c.sum() == a + b

        def test_constructor_five_per_five_sums(self):
            for a in range(10):
                for b in range(10):
                    sum_c = SumCircuit(a, b)
                    assert sum_c.sum() == a + b
