from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def test_installation():
    """
    Verify Qiskit installation and basic functionality
    """
    # Create a simple quantum circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate
    qc.measure(0, 0)

    # Run the circuit on the simulator
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    print("Installation test results:", counts)
    return counts

if __name__ == "__main__":
    test_installation()