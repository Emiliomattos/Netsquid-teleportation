import numpy as np


def pure_target_fidelity(rho, target_rho):
    """
    Fidelity with respect to a pure target state.

    If the target density matrix corresponds to a pure state,
    then the fidelity simplifies to:

        F = Tr(target_rho @ rho)

    This is convenient here because the ideal Bell pair and
    ideal teleportation output are pure states.
    """
    value = np.trace(target_rho @ rho)
    return float(np.real_if_close(value))
