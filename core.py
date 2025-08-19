
from Pi0KernelCore.quantum.processor import QuantumProcessor
from Pi0KernelCore.mathematical.operators import MathematicalOperators

class Pi0Engine:
    def __init__(self, num_qubits=2):
        self.quantum = QuantumProcessor(num_qubits=num_qubits)
        self.math = MathematicalOperators()

    def run_quantum(self, operations):
        for op in operations:
            self.quantum.add_gate(**op)
        return self.quantum.run()

    def run_math(self, operation, *args, **kwargs):
        method = getattr(self.math, operation)
        return method(*args, **kwargs)
