import netsquid as ns
from netsquid.nodes import Node
from netsquid.components import QuantumProcessor, ClassicalChannel
from netsquid.components.qprocessor import PhysicalInstruction
from netsquid.components.instructions import (
    INSTR_H, INSTR_CNOT, INSTR_MEASURE, INSTR_X, INSTR_Z
)
from netsquid.qubits import qubitapi as qapi

from .teleportation_protocol import AliceTeleport, BobTeleport


def make_qprocessor(name: str, num_positions: int) -> QuantumProcessor:
    # Define a simple "ideal hardware" instruction set.
    # duration is in ns (simulation time units). Values here are arbitrary but consistent.
    phys_instructions = [
        PhysicalInstruction(INSTR_H, duration=1),
        PhysicalInstruction(INSTR_X, duration=1),
        PhysicalInstruction(INSTR_Z, duration=1),
        PhysicalInstruction(INSTR_CNOT, duration=2),
        PhysicalInstruction(INSTR_MEASURE, duration=2, parallel=True),
    ]
    return QuantumProcessor(name=name, num_positions=num_positions,
                           phys_instructions=phys_instructions)


def build_network():
    alice_qmem = make_qprocessor("alice_qmem", num_positions=2)
    bob_qmem = make_qprocessor("bob_qmem", num_positions=1)

    alice = Node("Alice", qmemory=alice_qmem)
    bob = Node("Bob", qmemory=bob_qmem)

    cchan = ClassicalChannel("cchan_A2B", length=1e-3)
    alice.add_ports(["c_out"])
    bob.add_ports(["c_in"])
    alice.ports["c_out"].connect(cchan.ports["send"])
    bob.ports["c_in"].connect(cchan.ports["recv"])

    return alice, bob


def load_qubits(alice, bob):
    # Message qubit: |+> = H|0>
    q_msg = qapi.create_qubits(1)[0]
    qapi.operate(q_msg, ns.H)

    # Save target as density matrix for fidelity check
    target_dm = qapi.reduced_dm(q_msg)

    # EPR pair
    qA, qB = qapi.create_qubits(2)
    qapi.operate(qA, ns.H)
    qapi.operate([qA, qB], ns.CNOT)

    alice.qmemory.put([q_msg], positions=[0])
    alice.qmemory.put([qA], positions=[1])
    bob.qmemory.put([qB], positions=[0])

    return target_dm


def build_protocols(alice, bob):
    alice_p = AliceTeleport(alice, cport_name="c_out")
    bob_p = BobTeleport(bob, cport_name="c_in")
    return alice_p, bob_p
