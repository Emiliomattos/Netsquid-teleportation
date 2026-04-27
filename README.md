# NetSquid Quantum Teleportation & Noise Analysis

This project simulates quantum teleportation and entanglement using **NetSquid**, and extends the models to analyze how **noise affects quantum systems** using density matrices and fidelity.

---

## Overview

This project is structured in three stages:

### 1. Ideal Quantum Protocols
- Bell pair generation
- Quantum teleportation using NetSquid

### 2. Sampling Framework
- Extract density matrices from simulations
- Sample measurement outcomes without rerunning simulations
- Generate frequency tables and histograms

### 3. Noise & Fidelity Analysis
- Add depolarizing noise models
- Analyze how noise degrades quantum states
- Measure fidelity vs noise strength

---

## Key Concepts

- **Density Matrix Formalism**
  - Used to represent noisy quantum states
- **Depolarizing Noise**
  - Models decoherence in real quantum systems
- **Fidelity**
  - Measures similarity between noisy and ideal states
- **Sampling vs Simulation**
  - Run simulation once, sample many times

---

## Project Structure

```
netsquid-teleportation/
│
├── bell_pair_once.py
├── teleportation_once.py
│
├── bell_noise_sweep.py
├── teleportation_noise_sweep.py
│
├── ns_sampling/
│   ├── measure.py
│   ├── noise.py
│   └── fidelity.py
│
├── src/
│   ├── network.py
│   ├── protocols.py
│   └── ...
│
└── README.md
```

---

## How to Run

### 1. Activate Environment

```bash
cd ~/Desktop/netsquid-teleportation
source venv/bin/activate
```

---

### 2. Bell Pair Simulation

```bash
python bell_pair_once.py
```

Outputs:
- Density matrix
- Probability table
- Sample list
- Frequency table
- Histogram

---

### 3. Teleportation Simulation

```bash
python teleportation_once.py
```

Outputs:
- NetSquid simulation stats
- Bob’s final density matrix
- Measurement distribution
- Histogram

---

### 4. Noise Analysis

#### Bell Pair Sweep

```bash
python bell_noise_sweep.py
```

#### Teleportation Sweep

```bash
python teleportation_noise_sweep.py
```

Outputs:
- Fidelity vs depolarizing noise
- Graphs saved as `.png`

---

## Results

### Bell Pair

- Fidelity starts at **1.0** (perfect entanglement)
- Decreases as noise increases
- Approaches **0.25** at high noise

This corresponds to a **maximally mixed 2-qubit state**.

---

### Teleportation

- Fidelity starts near **1.0**
- Decreases as noise increases
- Approaches **0.5** at high noise

This corresponds to a **maximally mixed 1-qubit state**.

---

## Key Insight

Noise reduces coherence and transforms pure quantum states into mixed states.

- Bell pair → loses entanglement  
- Teleportation → loses accuracy  

Fidelity provides a clear quantitative measure of this degradation.

---

## Example Output

```
Depolarizing Rate    Fidelity
0.0000e+00           1.000000
1.0000e+06           0.864048
1.0000e+07           0.351501
1.0000e+08           0.250000
```

---

## Author

Emilio Mattos  
University of Vermont  
Quantum Networks Research
