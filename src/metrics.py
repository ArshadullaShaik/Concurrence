"""Count the cost of a compiled circuit."""
import math


def circuit_metrics(qc):
    ops = qc.count_ops()
    two_q = {"cx", "cz", "ecr", "swap", "rxx", "ryy", "rzz"}
    return {
        "depth": qc.depth(),
        "two_qubit_gates": sum(n for g, n in ops.items() if g in two_q),
        "swap_gates_left": ops.get("swap", 0),
        "total_ops": sum(ops.values()),
        "operations": dict(ops),
    }


def success_rate(counts, expected):
    total = sum(counts.values())
    return counts.get(expected, 0) / total


def proportion_standard_error(p, n):
    return math.sqrt(p * (1 - p) / n)
