<p align="center">
    <img src="https://raw.githubusercontent.com/TendTo/QCLight/master/docs/source/_static/img/logo.svg" width="200" height="200" />
</p>

Simple and lightweight Quantum Computing simulator built with python3 for educational purposes.

---

[![Deploy CI](https://github.com/TendTo/QCLight/actions/workflows/deploy.yml/badge.svg)](https://github.com/TendTo/QCLight/actions/workflows/deploy.yml)

## 🐍 Installation

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

## 💻 Local development

### 🧾 Requirements

- [python 3.7+](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)

### 🔧 Setup

Install the package locally with **pip**

> ℹ️ You may want to use a virtual local environment to install all your dependencies in.
> There are many options, but the simplest one is creating a venv environment with `python3 -m venv .venv`.
> Make sure to activate the environment with `source .venv/bin/activate`.
> If you are on Windows or want more information, follow this [guide](https://docs.python.org/3/library/venv.html).

```shell
# install the package requirements
pip3 install -r requirements.txt
# install the qclight package locally
pip3 install -e .
```

> ⚠️ Some older versions of pip do not support the -e \[--editable\] flag.
> The package can still be installed locally, but any change made to it requires a new installation
> to be properly visible.

## 🧪 Tests

Make sure to follow the [setup](#local-development) section beforehand.

```shell
# install development requirements
pip3 install -r requirements_dev.txt
# run the linter
pylint src/qclight
# run the tests
pytest
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
