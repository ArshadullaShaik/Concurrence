"""The problem: add two numbers with a quantum circuit (1-bit half adder)."""
from qiskit import QuantumCircuit


def one_bit_adder(a, b):
    """Qubits: 0=a, 1=b, 2=sum, 3=carry. Output bits read as 'carry sum'."""
    qc = QuantumCircuit(4, 2)
    if a:
        qc.x(0)
    if b:
        qc.x(1)
    qc.ccx(0, 1, 3)   # carry = a AND b
    qc.cx(0, 2)       # sum = a XOR b
    qc.cx(1, 2)
    qc.measure(2, 0)
    qc.measure(3, 1)
    return qc


def expected_output(a, b):
    """Correct answer as the 2-bit string 'carry sum'."""
    return format(a + b, "02b")

def two_bit_adder(a, b):
    """Adds two 2-bit numbers, answer mod 4. 5 qubits.
    Qubits: 0=a0, 1=a1, 2=b0, 3=b1, 4=carry. Result is left in b (b1 b0)."""
    qc = QuantumCircuit(5, 2)
    if a & 1: qc.x(0)
    if a & 2: qc.x(1)
    if b & 1: qc.x(2)
    if b & 2: qc.x(3)
    qc.ccx(0, 2, 4)   # carry from bit 0 = a0 AND b0
    qc.cx(0, 2)       # b0 = a0 XOR b0
    qc.cx(1, 3)       # b1 = a1 XOR b1
    qc.cx(4, 3)       # b1 = b1 XOR carry
    qc.measure(2, 0)
    qc.measure(3, 1)
    return qc


def expected_two_bit(a, b):
    return format((a + b) % 4, "02b")