# QFF 2026 Phase 1 - PS-P3

**Team:** Boring dudes  **Track:** Post-Quantum Cryptography  **Problem Statement:** P3 (see "Assumptions")

## What this project does
We build a small quantum adder circuit, run the *same* circuit on two simulated processors
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
- Noise values are our own simple choices, identical on A and B so wiring is the only difference.
- Transpiler settings (optimization level, seed) are fixed and recorded in the results.
- P3 interpretation: the Drive PDFs list P3 as "PQC Performance Benchmark" only; the website describes
  "Reversible Quantum Arithmetic & Carry-Chain Bottlenecks". We benchmark quantum adders.

## Results
(fill in from `results/tables/`)

## Files
See the folder tree. Analysis and limitations are in `report.md`.

## AI assistance disclosure
(State how AI tools were used, per the organizers' policy.)
