# pylint: disable=missing-function-docstring,too-few-public-methods
import pytest
import numpy as np
from qclight.error import BinaryStringError, PowerOfTwoLengthError, PositiveValueError
from qclight.circuit import QCLCircuit


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

    class TestSumCircuit:
        pass
