import numpy as np
import netsquid as ns
from collections import Counter
from netsquid.nodes import Node
from netsquid.components import QuantumProcessor
from netsquid.components.qprocessor import PhysicalInstruction
from netsquid.components.instructions import (
    INSTR_H,
    INSTR_CNOT,
    INSTR_MEASURE,
    INSTR_X,
    INSTR_Z,
)
from netsquid.qubits import qubitapi as qapi


def make_qprocessor(name: str, n: int) -> QuantumProcessor:
    """Create an ideal quantum processor with the required instruction set."""
    phys = [
        PhysicalInstruction(INSTR_H, duration=1),
        PhysicalInstruction(INSTR_X, duration=1),
        PhysicalInstruction(INSTR_Z, duration=1),
        PhysicalInstruction(INSTR_CNOT, duration=2),
        PhysicalInstruction(INSTR_MEASURE, duration=2, parallel=True),
    ]
    return QuantumProcessor(name=name, num_positions=n, phys_instructions=phys)


def bell_pair():
    """Create a Bell pair in the |Phi+> state."""
    q1, q2 = qapi.create_qubits(2)
    qapi.operate(q1, ns.H)
    qapi.operate([q1, q2], ns.CNOT)
    return q1, q2


def _event(retval):
    """
    Extract the EventExpression from the return value of
    QuantumProcessor.execute_instruction.
    """
    if retval.__class__.__name__ == "EventExpression":
        return retval

    if isinstance(retval, tuple):
        for item in retval:
            if getattr(item, "__class__", None) and item.__class__.__name__ == "EventExpression":
                return item
        return retval[-1]

    if isinstance(retval, dict):
        for value in retval.values():
            if getattr(value, "__class__", None) and value.__class__.__name__ == "EventExpression":
                return value

    raise TypeError(f"Could not extract EventExpression from: {retval}")


def _meas_bit(retval):
    """
    Extract a single measurement outcome bit from the return value of
    QuantumProcessor.execute_instruction for INSTR_MEASURE.
    """
    if isinstance(retval, tuple):
        for item in retval:
            if isinstance(item, dict) and "last" in item:
                return int(item["last"][0])

    if isinstance(retval, dict) and "last" in retval:
        return int(retval["last"][0])

    raise TypeError(f"Could not extract measurement bit from: {retval}")


def run_once():
    """
    Execute one entanglement swapping trial.

    Initial state:
        - Alice and Charlie share one Bell pair
        - Charlie and Bob share one Bell pair

    Charlie performs a Bell-state measurement on his two qubits.
    Conditional corrections are applied to Bob's qubit so that the
    final remote Alice-Bob state is standardized to |Phi+>.
    """
    ns.sim_reset()

    alice = Node("Alice", qmemory=make_qprocessor("alice_mem", 1))
    charlie = Node("Charlie", qmemory=make_qprocessor("charlie_mem", 2))
    bob = Node("Bob", qmemory=make_qprocessor("bob_mem", 1))

    qA, qC1 = bell_pair()
    qC2, qB = bell_pair()

    alice.qmemory.put([qA], positions=[0])
    charlie.qmemory.put([qC1], positions=[0])
    charlie.qmemory.put([qC2], positions=[1])
    bob.qmemory.put([qB], positions=[0])

    # Bell-state measurement at Charlie
    r = charlie.qmemory.execute_instruction(INSTR_CNOT, qubit_mapping=[0, 1])
    yield _event(r)

    r = charlie.qmemory.execute_instruction(INSTR_H, qubit_mapping=[0])
    yield _event(r)

    r0 = charlie.qmemory.execute_instruction(INSTR_MEASURE, qubit_mapping=[0])
    yield _event(r0)
    m0 = _meas_bit(r0)

    r1 = charlie.qmemory.execute_instruction(INSTR_MEASURE, qubit_mapping=[1])
    yield _event(r1)
    m1 = _meas_bit(r1)

    outcome = (m0, m1)

    # Feed-forward corrections to standardize the remote state
    if m1 == 1:
        r = bob.qmemory.execute_instruction(INSTR_X, qubit_mapping=[0])
        yield _event(r)

    if m0 == 1:
        r = bob.qmemory.execute_instruction(INSTR_Z, qubit_mapping=[0])
        yield _event(r)

    qA_final = alice.qmemory.peek([0])[0]
    qB_final = bob.qmemory.peek([0])[0]
    rho_AB = qapi.reduced_dm([qA_final, qB_final])

    return outcome, rho_AB


def main(N=200):
    """Run multiple entanglement swapping trials and average the remote density matrix."""
    outcomes = Counter()
    rho_sum = np.zeros((4, 4), dtype=complex)

    for _ in range(N):
        gen = run_once()

        try:
            while True:
                next(gen)
                ns.sim_run()
        except StopIteration as e:
            outcome, rho = e.value

        outcomes[outcome] += 1
        rho_sum += rho

    rho_avg = rho_sum / N

    print(f"Entanglement swapping: {N} runs")
    print("Charlie Bell-measurement outcomes (m0 m1):")
    for k in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        print(f"  {k[0]}{k[1]}: {outcomes[k] / N:.3f}")

    np.set_printoptions(precision=3, suppress=True)
    print("\nAverage remote density matrix rho_AB (after correction -> |Phi+>):")
    print(rho_avg.real)

    max_im = float(np.max(np.abs(rho_avg.imag)))
    print(f"\nMax |imag| element: {max_im:.3e}")


if __name__ == "__main__":
    main()
