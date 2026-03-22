import numpy as np
from collections import Counter

# Bell state: (|00> + |11>) / sqrt(2)
state = np.array([
    1/np.sqrt(2),
    0,
    0,
    1/np.sqrt(2)
], dtype=complex)

labels = ["00", "01", "10", "11"]

# Convert amplitudes to probabilities
probs = np.abs(state)**2

print("Statevector:")
for l, a in zip(labels, state):
    print(f"{l}: {a}")

print("\nProbabilities:")
for l, p in zip(labels, probs):
    print(f"{l}: {p}")

# Sample from distribution
N = 100
samples = np.random.choice(labels, size=N, p=probs)

# Frequency table
freq = Counter(samples)

print("\nFrequency table:")
print(freq)
