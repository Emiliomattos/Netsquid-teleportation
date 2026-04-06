import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def basis_labels(num_qubits):
    return [format(i, f"0{num_qubits}b") for i in range(2 ** num_qubits)]


def probabilities_from_density_matrix(rho):
    """
    Extract measurement probabilities in the computational basis
    from the diagonal of the density matrix.
    """
    diag = np.real(np.diag(rho))
    diag = np.clip(diag, 0.0, None)
    total = diag.sum()
    if total == 0:
        raise ValueError("Density matrix diagonal sums to zero.")
    return diag / total


def sample_density_matrix(rho, num_samples, rng=None):
    """
    Sample computational-basis measurement outcomes from a density matrix.
    """
    if rng is None:
        rng = np.random.default_rng()

    dim = rho.shape[0]
    num_qubits = int(np.log2(dim))
    labels = basis_labels(num_qubits)
    probs = probabilities_from_density_matrix(rho)
    samples = rng.choice(labels, size=num_samples, p=probs)
    return list(samples)


def frequency_table(samples, labels=None):
    counts = Counter(samples)
    if labels is None:
        return dict(counts)
    return {label: counts.get(label, 0) for label in labels}


def probability_table(rho):
    dim = rho.shape[0]
    num_qubits = int(np.log2(dim))
    labels = basis_labels(num_qubits)
    probs = probabilities_from_density_matrix(rho)
    return {label: float(prob) for label, prob in zip(labels, probs)}


def plot_histogram(freq_table, title="Measurement Outcome Histogram", save_path=None):
    labels = list(freq_table.keys())
    counts = list(freq_table.values())

    plt.figure(figsize=(8, 4))
    plt.bar(labels, counts)
    plt.xlabel("Measurement outcome")
    plt.ylabel("Count")
    plt.title(title)
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=200)

    plt.show()


def print_density_matrix(rho, decimals=3):
    np.set_printoptions(precision=decimals, suppress=True)
    print(rho.real)
