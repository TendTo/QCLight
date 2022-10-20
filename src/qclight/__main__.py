"""Main"""
import sys
from qclight.circuit import QCLCircuit


def main():
    """Simple main function"""
    circuit = QCLCircuit(2)
    circuit.show()

    if len(sys.argv) > 1:
        print(f"Args: {sys.argv[1:]}")
    else:
        print("No args")


if __name__ == "__main__":
    main()
