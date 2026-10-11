# Report

## Problem Statement
PS-P3: PQC Performance Benchmark / Reversible Quantum Arithmetic & Carry-Chain Bottlenecks.
We benchmark a 2-bit quantum modular adder (ripple-carry) on two simulated processors
with different wiring, measuring how connectivity affects routing overhead (SWAPs,
two-qubit gates, depth) and success rate.

## Method
- Build a 2-bit modular adder circuit (5 qubits: 2 for operand a, 2 for operand b, 1 carry).
- Transpile with identical settings (basis gates, optimization level, seed) for Processor A and B.
- Run ideal (noiseless) and noisy simulations with the same noise model on both.
- Repeat across 30 transpiler seeds to show the result is not a fluke.
- Also test a Draper (QFT) adder for comparison.
- Also sweep 300 random initial layouts to test placement sensitivity.

## Processor A
- 5 qubits, T-shaped fixed baseline graph.
- Coupling: 0-1, 1-2, 1-3, 3-4.
- Max degree: 3 (qubit 1). Diameter: 3.
- Basis gates: rz, sx, x, cx.

## Processor B
- 9 qubits, heavy-hex-inspired fragment.
- Coupling: 0-1, 1-2, 2-7, 1-3, 3-5, 4-5, 5-6, 6-8.
- Max degree: 3. Diameter: 5.
- Same basis gates and noise as A.

## A vs B
At optimization level 0 (default placement):
- B needs 24.4 mean 2Q gates vs A's 21.2 (over 30 seeds).
- B's depth is 31.9 vs A's 29.0.
- Noisy success: A 0.849, B 0.840.

At optimization level 1 (smart placement):
- Both need exactly 10 2Q gates. The gap disappears.

## Explanation (which processor property explains the difference?)
The carry qubit (q4) must interact with q0, q2, and q3. On A's T-graph, the default
logical-to-physical placement puts these qubits close together. On B's larger heavy-hex
fragment, they are farther apart, so the transpiler inserts more SWAPs (each costs 3 CX
gates). The placement sweep confirms B has many more bad layout choices (max 45 gates vs
A's 24), so the default placement is more likely to be poor on B.

The key insight: **the wiring gap is real at level 0, but a good compiler (level 1) can
hide it entirely for a small circuit.** The architecture advantage only shows up when
the circuit is large enough that even smart placement cannot avoid long-range interactions.

## Evidence (which table or figure supports it?)
- `results/tables/seed_sweep.csv`: 30-seed means show B > A at level 0, equal at level 1.
- `results/tables/design_comparison.csv`: Ripple (10 gates) beats Draper (19 gates) at level 1.
- `results/tables/layout_sweep.csv`: B's placement spread (15–45) far exceeds A's (12–24).
- `results/tables/scaling_trend.csv`: Gate count grows from 17 (1-bit) to 24 (2-bit) to 59 (3-bit) on B.
- `results/figures/processor_A_graph.png` and `processor_B_graph.png`: visual comparison.
- `results/figures/scaling_trend.png`: line chart showing gate growth with adder size.

## Additional Experiments

**Noise sensitivity:** As 2Q error increases from 0.5% to 5%, the A–B success-rate gap widens from 0.4% to 2.8%. B's extra gates cause steeper noise degradation, confirming that the routing overhead has a measurable cost beyond just gate count.

**Multiplier:** A 2-bit multiplier (6 qubits, 48 2Q gates) runs on B only (does not fit on A's 5 qubits). Ideal success rate is 1.0; noisy success rate is 0.778. This extends the benchmark beyond adders to a second arithmetic operation.

## Scope and Future Work

This project benchmarks two adder designs (ripple-carry and Draper QFT) on two small simulated processors. The results show that wiring affects routing cost at low optimization levels, and that this effect grows with circuit size.

Future work could extend this by:
- Testing on real quantum hardware (IBM Quantum backends)
- Adding more circuit families (Grover, QFT, variational circuits)
- Scaling to larger processors (15-25 qubits) where routing effects are more pronounced
- Using realistic noise models calibrated from actual device properties
