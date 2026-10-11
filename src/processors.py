"""Load a processor JSON and turn it into Qiskit objects."""
import json
from pathlib import Path
from qiskit.transpiler import CouplingMap
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError


def load_processor(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def get_coupling_map(proc):
    """JSON edges are undirected, so add both directions."""
    edges = []
    for a, b in proc["coupling_map"]:
        edges += [[a, b], [b, a]]
    return CouplingMap(edges)


def get_noise_model(proc):
    n = proc["noise"]
    model = NoiseModel()
    model.add_all_qubit_quantum_error(depolarizing_error(n["one_qubit_gate_error"], 1), ["x", "sx"])
    model.add_all_qubit_quantum_error(depolarizing_error(n["two_qubit_gate_error"], 2), ["cx"])
    p = n["readout_error"]
    model.add_all_qubit_readout_error(ReadoutError([[1 - p, p], [p, 1 - p]]))
    return model
