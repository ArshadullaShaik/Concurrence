"""Compile (transpile) a circuit for a processor, run it, and collect results."""
from qiskit import transpile
from qiskit_aer import AerSimulator
from .processors import get_coupling_map, get_noise_model
from .metrics import circuit_metrics


def compile_for(circuit, proc, optimization_level=0, seed=1):
    """Same settings for every processor. Record them in the results."""
    return transpile(
        circuit,
        coupling_map=get_coupling_map(proc),
        basis_gates=proc["basis_gates"],
        optimization_level=optimization_level,
        seed_transpiler=seed,
    )


def run_on(circuit, proc, shots=2048, noisy=True, optimization_level=0, seed=1):
    compiled = compile_for(circuit, proc, optimization_level, seed)
    sim = AerSimulator(noise_model=get_noise_model(proc)) if noisy else AerSimulator()
    counts = sim.run(compiled, shots=shots, seed_simulator=seed).result().get_counts()
    return compiled, counts, circuit_metrics(compiled)
