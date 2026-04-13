import netsquid as ns


def apply_depolarizing_noise(qubit, depolar_rate, delay=1):
    """
    Apply NetSquid depolarizing noise to a qubit.

    depolar_rate: noise rate in Hz
    delay: effective waiting time / duration
    """
    ns.qubits.delay_depolarize(qubit, depolar_rate=depolar_rate, delay=delay)
