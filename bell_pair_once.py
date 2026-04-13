import netsquid as ns
from netsquid.qubits import qubitapi as qapi
from ns_sampling.noise import apply_depolarizing_noise
from ns_sampling.measure import (
    sample_density_matrix,
    frequency_table,
    probability_table,
    basis_labels,
    plot_histogram,
    print_density_matrix,
)


def build_bell_pair_density_matrix(depolar_rate=0, delay=1):
    """
    Create a Bell pair in NetSquid and return its 2-qubit density matrix.
    Optional depolarizing noise can be applied before measurement.
    """
    q1, q2 = qapi.create_qubits(2)
    qapi.operate(q1, ns.H)
    qapi.operate([q1, q2], ns.CNOT)

    if depolar_rate > 0:
        apply_depolarizing_noise(q1, depolar_rate=depolar_rate, delay=delay)
        apply_depolarizing_noise(q2, depolar_rate=depolar_rate, delay=delay)

    rho = qapi.reduced_dm([q1, q2])
    return rho


def main(num_samples=100, depolar_rate=0, delay=1):
    rho = build_bell_pair_density_matrix(depolar_rate=depolar_rate, delay=delay)

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
    main(num_samples=100, depolar_rate=1e7, delay=1)
