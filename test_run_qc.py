# General
import numpy as np

# Qiskit imports
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp

# Qiskit Runtime imports
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# Plotting routines
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram

QiskitRuntimeService.save_account(

    channel="ibm_quantum",

    token="55ddbddb007bbc07e4b093124f1045491e393a53ee5df189375485aa3e4e33fc9e90c452f81d22915a766d4a8b262ec3cdcfa1d2ca90c84255b57a144cf14c4d",

    set_as_default=True,

    # Use `overwrite=True` if you're updating your token.
    overwrite=True,
)

service = QiskitRuntimeService()

service = QiskitRuntimeService(channel="ibm_quantum")
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
print(backend)

pass_manager = generate_preset_pass_manager(
    optimization_level=3, backend=backend
)

sampler = Sampler(mode=backend)

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# 4. Transpile circuit
transpiled_qc = pass_manager.run(qc)

# 5. Run on real hardware

job = sampler.run([transpiled_qc])
print("Job ID:", job.job_id())
result = job.result()[0]
counts = result.join_data().get_counts()


print("Counts from hardware:", counts)

# # 6. Plot the result
plot_histogram(counts)
plt.show()

