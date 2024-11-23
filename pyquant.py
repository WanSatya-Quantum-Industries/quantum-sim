from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import numpy as np

class QuantumSimulator:
    def __init__(self, num_qubits):
        """
        Initialize quantum simulator with specified number of qubits
        """
        self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(num_qubits, num_qubits)  # quantum and classical registers
        self.simulator = AerSimulator()
    
    def apply_hadamard(self, qubit):
        """
        Apply Hadamard gate to create superposition
        """
        self.circuit.h(qubit)
        return self
    
    def apply_cnot(self, control_qubit, target_qubit):
        """
        Apply CNOT gate between two qubits
        """
        self.circuit.cx(control_qubit, target_qubit)
        return self
    
    def apply_phase(self, qubit, angle):
        """
        Apply phase rotation
        """
        self.circuit.rz(angle, qubit)
        return self
    
    def measure_qubit(self, qubit, classical_bit):
        """
        Measure specific qubit
        """
        self.circuit.measure(qubit, classical_bit)
        return self
    
    def measure_all(self):
        """
        Measure all qubits
        """
        for i in range(self.num_qubits):
            self.circuit.measure(i, i)
        return self
    
    def run(self, shots=1000):
        """
        Execute the quantum circuit and return results
        """
        job = self.simulator.run(self.circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(self.circuit)
        return counts
    
    def create_bell_pair(self):
        """
        Create a Bell pair (maximally entangled state)
        """
        self.apply_hadamard(0)
        self.apply_cnot(0, 1)
        return self
    
    def quantum_teleportation(self, state_to_teleport):
        """
        Implement quantum teleportation protocol
        Assumes 3 qubits where:
        - Qubit 0: State to teleport
        - Qubit 1 & 2: Bell pair for teleportation channel
        """
        # Prepare the state to teleport
        if state_to_teleport[0] != 0:
            self.circuit.x(0)
        if state_to_teleport[1] != 0:
            self.circuit.rz(state_to_teleport[1], 0)
            
        # Create Bell pair between qubits 1 and 2
        self.circuit.h(1)
        self.circuit.cx(1, 2)
        
        # Perform teleportation
        self.circuit.cx(0, 1)
        self.circuit.h(0)
        
        # Measure qubits 0 and 1
        self.circuit.measure([0, 1], [0, 1])
        
        return self