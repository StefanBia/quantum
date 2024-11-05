from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit_ibm_provider.job import job_monitor
import matplotlib.pyplot as plt
from qiskit.visualization import plot_distribution

# Load the IBM Quantum service (this assumes you saved the account with channel='ibm_quantum')
service = QiskitRuntimeService()

# Select an IBM Quantum backend, e.g., 'ibmq_manila'
backend = service.backend('ibm_kyiv')  # Replace with an available backend

# Create and initialize a quantum circuit
circuit = QuantumCircuit(4)
initial_state = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
circuit.initialize(initial_state, [0, 1, 2, 3])

# Apply gates
circuit.x(0)
circuit.ccx(0, 1, 3)
circuit.ccx(0, 1, 2)
circuit.x(0)
circuit.x(1)
circuit.ccx(0, 1, 2)
circuit.x(1)

# Draw the circuit
circuit.draw('mpl')
plt.show()

# Add measurements to all qubits
circuit.measure_all()

# Transpile the circuit for the backend
compiled_circuit = transpile(circuit, backend)

sampler = SamplerV2(mode=backend)
sampler.options.default_shots = 256
# Execute the circuit on the selected backend
result = sampler.run([compiled_circuit]).result()
dist = result[0].data.meas.get_counts()

plot_distribution(dist)
