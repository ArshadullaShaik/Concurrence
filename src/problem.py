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

def draper_adder_2bit(a, b):
    """2-bit Draper (QFT) adder, answer mod 4. 4 qubits, no ancilla.
    Qubits: 0=a0, 1=a1, 2=b0, 3=b1. Result is left in b (b1 b0)."""
    import math
    qc = QuantumCircuit(4, 2)
    if a & 1: qc.x(0)
    if a & 2: qc.x(1)
    if b & 1: qc.x(2)
    if b & 2: qc.x(3)
    qc.h(3); qc.cp(math.pi / 2, 2, 3); qc.h(2); qc.swap(2, 3)   # QFT on b
    for j in range(2):
        for k in range(2):
            angle = 2 * math.pi * 2**j * 2**k / 4
            if abs(angle % (2 * math.pi)) > 1e-9:
                qc.cp(angle, j, 2 + k)
    qc.swap(2, 3); qc.h(2); qc.cp(-math.pi / 2, 2, 3); qc.h(3)  # inverse QFT
    qc.measure(2, 0)
    qc.measure(3, 1)
    return qc


def three_bit_adder(a, b):
    """Adds two 3-bit numbers, answer mod 8. 8 qubits.
    Qubits: 0=a0, 1=a1, 2=a2, 3=b0, 4=b1, 5=b2, 6=carry0, 7=carry1.
    Result is left in b (b2 b1 b0)."""
    qc = QuantumCircuit(8, 3)
    if a & 1: qc.x(0)
    if a & 2: qc.x(1)
    if a & 4: qc.x(2)
    if b & 1: qc.x(3)
    if b & 2: qc.x(4)
    if b & 4: qc.x(5)
    # Bit 0
    qc.ccx(0, 3, 6)   # carry0 = a0 AND b0
    qc.cx(0, 3)       # b0 = a0 XOR b0
    # Bit 1
    qc.cx(1, 4)       # b1 = a1 XOR b1
    qc.cx(6, 4)       # b1 = b1 XOR carry0
    qc.ccx(1, 4, 7)   # carry1 = (a1 XOR b1) AND carry0 ... simplified
    # Bit 2
    qc.cx(2, 5)       # b2 = a2 XOR b2
    qc.cx(7, 5)       # b2 = b2 XOR carry1
    qc.measure(3, 0)
    qc.measure(4, 1)
    qc.measure(5, 2)
    return qc


def expected_three_bit(a, b):
    return format((a + b) % 8, "03b")


def two_bit_multiplier(a, b):
    """Multiplies two 2-bit numbers, answer mod 4. 6 qubits.
    Qubits: 0=a0, 1=a1, 2=b0, 3=b1, 4=p0, 5=p1. Result is left in p (p1 p0).
    For mod 4: p0 = a0*b0, p1 = (a0*b1) XOR (a1*b0). The a1*b1 term is dropped."""
    qc = QuantumCircuit(6, 2)
    if a & 1: qc.x(0)
    if a & 2: qc.x(1)
    if b & 1: qc.x(2)
    if b & 2: qc.x(3)
    # Partial products for mod 4 result
    qc.ccx(0, 2, 4)   # p0 = a0 AND b0
    qc.ccx(0, 3, 5)   # p1 = a0 AND b1
    qc.ccx(1, 2, 5)   # p1 ^= a1 AND b0 (XOR via consecutive Toffolis on same target)
    qc.measure(4, 0)
    qc.measure(5, 1)
    return qc


def expected_mult(a, b):
    return format((a * b) % 4, "02b")