"""Main"""
from qclight.circuit import QCLVisualCircuit


def main():
    """Simple main function"""
    circuit = QCLVisualCircuit(4)
    circuit.h(0)
    circuit.cx(0, 3)
    circuit.barrier()
    circuit.x(2)
    print(circuit)


if __name__ == "__main__":
    main()
