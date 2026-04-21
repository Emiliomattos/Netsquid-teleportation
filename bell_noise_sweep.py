import matplotlib.pyplot as plt

from bell_pair_once import build_bell_pair_density_matrix
from ns_sampling.fidelity import pure_target_fidelity


def main(delay=100):
    rates = [0, 1e6, 1e7, 1e8, 1e9]

    target_rho = build_bell_pair_density_matrix(depolar_rate=0, delay=delay)

    fidelities = []
    print("Bell pair fidelity vs depolarizing noise")
    print(f"{'depolar_rate':>15}   {'fidelity':>10}")

    for rate in rates:
        rho = build_bell_pair_density_matrix(depolar_rate=rate, delay=delay)
        F = pure_target_fidelity(rho, target_rho)
        fidelities.append(F)
        print(f"{rate:15.4e}   {F:10.6f}")

    plt.figure(figsize=(8, 4))
    plt.plot(rates, fidelities, marker='o')
    plt.xscale("log")
    plt.xlabel("Depolarizing rate")
    plt.ylabel("Fidelity to ideal Bell state")
    plt.title("Bell Pair Fidelity vs Depolarizing Noise")
    plt.tight_layout()
    plt.savefig("bell_noise_sweep.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main(delay=100)
