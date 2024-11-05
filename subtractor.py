from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Initialize your account
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(instance="ibm-q/open/main")

service.backends()

circuit = QuantumCircuit(4)

initial_state = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
circuit.initialize(initial_state, [0, 1, 2, 3])

# Apply gates to the circuit
circuit.x(0)
circuit.ccx(0, 1, 3)
circuit.ccx(0, 1, 2)
circuit.x(0)
circuit.x(1)
circuit.ccx(0, 1, 2)
circuit.x(1)

circuit.draw('mpl')
plt.show()

simulator = AerSimulator()

# Transpile the circuit for the simulator

circuit.measure_all()

# Re-transpile the circuit with measurements
compiled_circuit = transpile(circuit, simulator)

# Run the simulation, specifying the number of shots (repetitions)
job = simulator.run(compiled_circuit, shots=1024)
result = job.result()

# Get the counts of the measurement results
counts = result.get_counts(compiled_circuit)
print(counts)

# Plot a histogram of the results
plot_histogram(counts)
plt.show()