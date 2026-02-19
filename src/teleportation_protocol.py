from netsquid.protocols import NodeProtocol
from netsquid.components.instructions import (
    INSTR_H, INSTR_CNOT, INSTR_MEASURE, INSTR_X, INSTR_Z
)

def _is_eventexpr(x):
    return x is not None and x.__class__.__name__ == "EventExpression"

def _get_eventexpr(result):
    # EventExpression directly
    if _is_eventexpr(result):
        return result

    # Tuple returns (often contains EventExpression somewhere)
    if isinstance(result, tuple):
        for item in result:
            if _is_eventexpr(item):
                return item
        # fallback
        return result[-1]

    # Dict returns (sometimes contains EventExpression as a value)
    if isinstance(result, dict):
        for v in result.values():
            if _is_eventexpr(v):
                return v

    raise TypeError(f"Unsupported execute_instruction return type: {type(result)} -> {result}")

def _extract_bit(val):
    if isinstance(val, (int, bool)):
        return int(val)
    if isinstance(val, (list, tuple)) and len(val) > 0 and isinstance(val[0], (int, bool)):
        return int(val[0])
    return None

def _get_measurement_outcome(result):
    """
    Your NetSquid MEASURE returns a tuple like:
      ({'last': [0], 'instr': [0]}, 2.0, EventExpression)

    Outcome bit is in dict['last'][0].
    """
    # If result is a tuple, scan elements for dict/list/int that contain the bit
    if isinstance(result, tuple):
        for item in result:
            if isinstance(item, dict):
                # Your observed key:
                if "last" in item:
                    bit = _extract_bit(item["last"])
                    if bit is not None:
                        return bit
                # Other possible keys (just in case)
                for k in ("outcome", "result", "results", "measurement", "m"):
                    if k in item:
                        bit = _extract_bit(item[k])
                        if bit is not None:
                            return bit
            else:
                bit = _extract_bit(item)
                if bit is not None:
                    return bit

    # If result is a dict directly
    if isinstance(result, dict):
        if "last" in result:
            bit = _extract_bit(result["last"])
            if bit is not None:
                return bit
        for k in ("outcome", "result", "results", "measurement", "m"):
            if k in result:
                bit = _extract_bit(result[k])
                if bit is not None:
                    return bit

    raise TypeError(f"Could not extract measurement outcome from: {result}")


class AliceTeleport(NodeProtocol):
    def __init__(self, node, cport_name="c_out"):
        super().__init__(node)
        self.qmem = node.qmemory
        self.cport = node.ports[cport_name]

    def run(self):
        r = self.qmem.execute_instruction(INSTR_CNOT, qubit_mapping=[0, 1])
        yield _get_eventexpr(r)

        r = self.qmem.execute_instruction(INSTR_H, qubit_mapping=[0])
        yield _get_eventexpr(r)

        r0 = self.qmem.execute_instruction(INSTR_MEASURE, qubit_mapping=[0])
        yield _get_eventexpr(r0)
        m0 = _get_measurement_outcome(r0)

        r1 = self.qmem.execute_instruction(INSTR_MEASURE, qubit_mapping=[1])
        yield _get_eventexpr(r1)
        m1 = _get_measurement_outcome(r1)

        self.cport.tx_output((m0, m1))


class BobTeleport(NodeProtocol):
    def __init__(self, node, cport_name="c_in"):
        super().__init__(node)
        self.qmem = node.qmemory
        self.cport = node.ports[cport_name]

    def run(self):
        yield self.await_port_input(self.cport)
        (m0, m1) = self.cport.rx_input().items[0]

        if m1 == 1:
            r = self.qmem.execute_instruction(INSTR_X, qubit_mapping=[0])
            yield _get_eventexpr(r)
        if m0 == 1:
            r = self.qmem.execute_instruction(INSTR_Z, qubit_mapping=[0])
            yield _get_eventexpr(r)
