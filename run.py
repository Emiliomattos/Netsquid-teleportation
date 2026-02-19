import netsquid as ns
from netsquid.qubits import qubitapi as qapi
from src.network import build_network, load_qubits, build_protocols

def main():
    ns.sim_reset()

    alice, bob = build_network()
    target = load_qubits(alice, bob)

    alice_p, bob_p = build_protocols(alice, bob)
    bob_p.start()
    alice_p.start()

    ns.sim_run()

    qb = bob.qmemory.peek([0])[0]
    F = qapi.fidelity(qb, target)
    print("Teleportation fidelity:", F)

if __name__ == "__main__":
    main()
