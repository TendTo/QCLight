"""Main"""
import sys
# from qclight.circuit import SumCircuit


def main():
    """Simple main function"""
    # sum = SumCircuit(0b101, 0b110)
    # print(sum.gates)
    sum.print_results()
    if len(sys.argv) > 1:
        print(f"Args: {sys.argv[1:]}")
    else:
        print("No args")


if __name__ == "__main__":
    main()
