"""Gate class"""
import numpy as np


class Gate:
    """Gates are the basic building blocks of quantum circuits.
    They are used to manipulate the state of a quantum system and compute functions.
    """

    I = np.array([[1, 0], [0, 1]])

    @property
    def matrix(self) -> "np.ndarray":
        """Matrix representation of the gate."""
        raise NotImplementedError("This method must be implemented by a subclass.")

    def matrix_of_size(
        self, size: "int", idx: "int | list[int] | None" = None
    ) -> "np.ndarray":
        """Returns the matrix representation of the gate in a matrix of size n x n,
        using the tensor product.

        If idx is None, the matrix is multiplied by itself.
        If idx is provided, the matrix is multiplied by the identity matrix
        in all the positions except for idx, where the matrix is multiplied by itself.

        Args:
            size: size of the matrix
            idx: index of the matrix in the tensor product

        Returns:
            matrix representation of the gate in a matrix of size n x n
        """
        if idx is None:
            return self.tp([self.matrix] * size)
        if isinstance(idx, int):
            idx = [idx]
        matrices = [self.I] * size
        for i in idx:
            matrices[i] = self.matrix
        return self.tp(matrices)

    def tp(self, gates: "list[np.ndarray]") -> "np.ndarray":
        """Calculates the tensor product between all the gates in the list.

        Args:
            gates: list of gates to be multiplied

        Raises:
            ValueError: the list of gates is empty

        Returns:
            the tensor product of all the gates in the list
        """
        if len(gates) == 0:
            raise ValueError("ql must not be empty")
        v = gates[0]
        for gate in gates[1:]:
            v = np.kron(v, gate)
        return v

    def __eq__(self, __o: object) -> bool:
        return self.__class__ is __o.__class__
