# General
import numpy as np

# Qiskit imports
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
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

    token="fef9c3c9cec270a5767a57eefa84b11a114bd4466c476d5cd43201aa18f152f4064c470a4db3e67f0374881ba1573dac174f7d34f2ac0703dc6bd8d90211d549",

    set_as_default=True,

    # Use `overwrite=True` if you're updating your token.
    overwrite=True,
)

# service = QiskitRuntimeService()

service = QiskitRuntimeService(channel="ibm_quantum")
backend = service.backend("ibm_sherbrooke")
print(backend)

pass_manager = generate_preset_pass_manager(
    optimization_level=3, backend=backend
)

sampler = Sampler(mode=backend)


qreg = QuantumRegister(5, 'q')
creg = ClassicalRegister(2, 'c')

qc = QuantumCircuit(qreg, creg)
qc.cx(qreg[0], qreg[1])
qc.cx(qreg[0], qreg[2])
qc.cx(qreg[0], qreg[3])
qc.cx(qreg[1], qreg[3])
qc.cx(qreg[1], qreg[4])
qc.cx(qreg[2], qreg[4])


qc.measure(qreg[3], creg[0])
qc.measure(qreg[4], creg[1])


with qc.if_test((creg, 0b01)):
    qc.x(qreg[0])  # Apply Z on qubit 0 if error on the first block

with qc.if_test((creg, 0b11)):
    qc.x(qreg[1])  # Apply Z on qubit 0 if error on second block

with qc.if_test((creg, 0b10)):
    qc.x(qreg[2])  # Apply Z on qubit 6 if error is on the final block

# 4. Transpile circuit
transpiled_qc = pass_manager.run(qc)

transpiled_qc.draw('mpl')
# 5. Run on real hardware

job = sampler.run([transpiled_qc], shots=10000)
print("Job ID:", job.job_id())
result = job.result()[0]
counts = result.join_data().get_counts()


print("Counts from hardware:", counts)

# # 6. Plot the result
plot_histogram(counts)
plt.show()

