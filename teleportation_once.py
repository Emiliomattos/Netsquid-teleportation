import netsquid as ns
from netsquid.qubits import qubitapi as qapi

from src.network import build_network, load_qubits, build_protocols
from ns_sampling.measure import (
    sample_density_matrix,
    frequency_table,
    probability_table,
    basis_labels,
    plot_histogram,
    print_density_matrix,
)


def build_teleportation_output_density_matrix():
    """
    Run the teleportation protocol once in NetSquid and return
    Bob's final 1-qubit density matrix.
    """
    ns.sim_reset()

    alice, bob = build_network()
    load_qubits(alice, bob)

    alice_p, bob_p = build_protocols(alice, bob)
    bob_p.start()
    alice_p.start()

    ns.sim_run()

    qb = bob.qmemory.peek([0])[0]
    rho = qapi.reduced_dm(qb)
    return rho


def main(num_samples=100):
    rho = build_teleportation_output_density_matrix()

    print("Teleportation output density matrix (Bob's qubit):")
    print_density_matrix(rho)

    probs = probability_table(rho)
    print("\nProbability table:")
    for label, prob in probs.items():
        print(f"  {label}: {prob:.4f}")

    samples = sample_density_matrix(rho, num_samples=num_samples)
    print(f"\nSample list ({num_samples} samples):")
    print(samples)

    freq = frequency_table(samples, labels=basis_labels(1))
    print("\nFrequency table:")
    print(freq)

    plot_histogram(
        freq,
        title=f"Teleportation Output Sampling Histogram ({num_samples} samples)",
        save_path="teleportation_histogram.png",
    )


if __name__ == "__main__":
    main(num_samples=100)
