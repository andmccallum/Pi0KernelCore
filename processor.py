
import numpy as np
import qutip as qt
from qutip_qip.circuit import QubitCircuit
from qutip_qip.operations import Gate

class QuantumProcessor:
    def __init__(self, num_qubits=2):
        self.num_qubits = num_qubits
        self.circuit = QubitCircuit(num_qubits)
        self.state = None

    def initialize_state(self, state_type='zero'):
        if state_type == 'zero':
            self.state = qt.basis([2] * self.num_qubits)
        elif state_type == 'plus':
            plus = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
            self.state = qt.tensor([plus] * self.num_qubits)
        return self.state

    def add_gate(self, gate_type, targets, controls=None, arg_value=None):
        gate = Gate(gate_type, targets, controls, arg_value)
        self.circuit.add_gate(gate)

    def run(self):
        if self.state is None:
            self.initialize_state()
        return self.circuit.run(self.state)

    def measure(self, targets):
        result = {}
        for t in targets:
            proj = qt.basis(2, 0) * qt.basis(2, 0).dag()
            op = qt.tensor([proj if i == t else qt.qeye(2) 
                          for i in range(self.num_qubits)])
            val = (self.state.dag() * op * self.state)
            if isinstance(val, qt.Qobj):
                prob = val.full().item().real
            else:
                prob = val.real
            result[f'qubit_{t}'] = prob
        return result
