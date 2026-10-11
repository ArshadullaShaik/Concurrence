# QFF 2026 Phase 1 - PS-P3

**Team:** Boring dudes  **Track:** Post-Quantum Cryptography  **Problem Statement:** P3 

## What this project does
We build a quantum adder circuit, run the circuit on two simulated processors
(A: 5 qubits, B: 9 qubits, heavy-hex-inspired), and measure how the processor wiring changes
depth, two-qubit gates, SWAP overhead and success rate.

## Setup
```
pip install -r requirements.txt
```
Open `main.ipynb` and run all cells top to bottom.

## Assumptions (what is official and what we chose)
- Official (organizer clarification): A = 5 qubits, fixed baseline graph, synthetic noise.
  B = 9 qubits, heavy-hex-inspired graph, contemporary compilation baseline.
- No official processor files exist; we designed both coupling maps ourselves (see `processors/`).
- Noise values are identical on A and B so wiring is the only difference.
- Transpiler settings (optimization level, seed) are fixed and recorded in the results.
- P3 interpretation: the Drive PDFs list P3 as "PQC Performance Benchmark" only; the website describes
  "Reversible Quantum Arithmetic & Carry-Chain Bottlenecks". We benchmark quantum adders.

## Results

### 2-bit adder, single seed (opt level 0)
| Processor | Noisy | Depth | 2Q gates | Success rate |
|-----------|-------|-------|----------|--------------|
| A         | No    | 28    | 21       | 1.000        |
| A         | Yes   | 28    | 21       | 0.849        |
| B         | No    | 31    | 24       | 1.000        |
| B         | Yes   | 31    | 24       | 0.840        |

### Seed sweep (30 seeds, 2-bit adder)
| Opt level | Processor | 2Q mean | 2Q SD | 2Q min | 2Q max | Depth mean |
|-----------|-----------|---------|-------|--------|--------|------------|
| 0         | A         | 21.2    | 0.8   | 21     | 24     | 29.0       |
| 0         | B         | 24.4    | 1.0   | 24     | 27     | 31.9       |
| 1         | A         | 10.0    | 0.0   | 10     | 10     | 20.0       |
| 1         | B         | 10.0    | 0.0   | 10     | 10     | 19.2       |

**Key finding:** At optimization level 0, B needs ~3 more two-qubit gates than A (24.4 vs 21.2). At level 1, both drop to 10 gates — the compiler hides the wiring gap.

### Design comparison (30 seeds, opt level 1)
| Design  | Processor | 2Q mean | Depth mean | Noisy success |
|---------|-----------|---------|------------|---------------|
| Ripple  | A         | 10.0    | 20.0       | 0.903         |
| Ripple  | B         | 10.0    | 19.2       | 0.903         |
| Draper  | A         | 19.0    | —          | 0.846         |
| Draper  | B         | 19.0    | —          | 0.846         |

### Placement sweep (300 random layouts, opt level 0)
| Processor | Min gates | Mean gates | Max gates |
|-----------|-----------|------------|-----------|
| A         | 12        | 18.6       | 24        |
| B         | 15        | 28.2       | 45        |

B's wider spread (15–45 vs 12–24) means more bad placements exist on the larger chip.

### Scaling trend (gate count vs adder size)
| Processor | Adder size | Qubits | 2Q gates | Depth |
|-----------|------------|--------|----------|-------|
| A         | 1-bit      | 4      | 17       | 29    |
| B         | 1-bit      | 4      | 17       | 29    |
| A         | 2-bit      | 5      | 21       | 28    |
| B         | 2-bit      | 5      | 24       | 31    |
| B         | 3-bit      | 8      | 59       | 57    |

A maxes out at 2-bit (5 qubits). B handles 3-bit (8 qubits) but at 59 gates —
the routing cost grows steeply with size on the heavy-hex fragment.

## Files
See the folder tree. Analysis and limitations are in `report.md`.

## Scope and Future Work

This project benchmarks two adder designs (ripple-carry and Draper QFT) on two small simulated processors. The results show that wiring affects routing cost at low optimization levels, and that this effect grows with circuit size.

Future work could extend this by:
- Testing on real quantum hardware (IBM Quantum backends)
- Adding more circuit families (Grover, QFT, variational circuits)
- Scaling to larger processors (15-25 qubits) where routing effects are more pronounced
- Using realistic noise models calibrated from actual device properties
