<p align="center">
    <img src="https://raw.githubusercontent.com/TendTo/QCLight/master/docs/source/_static/img/logo.svg" width="200" height="200" />
</p>

Simple and lightweight Quantum Computing simulator built with python3 for educational purposes.

---

[![Deploy CI](https://github.com/TendTo/QCLight/actions/workflows/deploy.yml/badge.svg)](https://github.com/TendTo/QCLight/actions/workflows/deploy.yml)

## Installation

```shell
pip install qclight
```

## Example

```python
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
```

## TODO

- [x] Improve performance with a custom range function for fixed bits
- [ ] Measure qubit
- [ ] Add more examples
- [x] Print ascii of circuit
- [ ] Print svg of circuit
- [ ] Circuit composition
- [ ] Circuit to gate
- [ ] SumCircuit
