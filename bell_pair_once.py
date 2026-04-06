import netsquid as ns
from netsquid.qubits import qubitapi as qapi

from ns_sampling.measure import (
    sample_density_matrix,
    frequency_table,
    probability_table,
    basis_labels,
    plot_histogram,
    print_density_matrix,
)


def build_bell_pair_density_matrix():
    """
    Create a Bell pair in NetSquid and return its 2-qubit density matrix.
    """
    q1, q2 = qapi.create_qubits(2)
    qapi.operate(q1, ns.H)
    qapi.operate([q1, q2], ns.CNOT)
    rho = qapi.reduced_dm([q1, q2])
    return rho


def main(num_samples=100):
    rho = build_bell_pair_density_matrix()

    print("Bell-pair density matrix:")
    print_density_matrix(rho)

    probs = probability_table(rho)
    print("\nProbability table:")
    for label, prob in probs.items():
        print(f"  {label}: {prob:.4f}")

    samples = sample_density_matrix(rho, num_samples=num_samples)
    print(f"\nSample list ({num_samples} samples):")
    print(samples)

    freq = frequency_table(samples, labels=basis_labels(2))
    print("\nFrequency table:")
    print(freq)

    plot_histogram(
        freq,
        title=f"Bell Pair Sampling Histogram ({num_samples} samples)",
        save_path="bell_pair_histogram.png",
    )


if __name__ == "__main__":
    main(num_samples=100)
