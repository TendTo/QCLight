<p align="center">
    <img src="./docs/source/_static/img/logo.svg" width="200" height="200" />
</p>

Simple and lightweight Quantum Computing simulator built with python3 for educational purposes.

---

## Installation

```shell
pip install qclight
```

## Example

```python
from qclight.circuit import QCLCircuit


def main():
    circuit = QCLCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.run()


if __name__ == "__main__":
    main()
```
