from qiskit import *
from qiskit.visualization import *
from qiskit_textbook.tools import *
from qiskit.extensions import *
from qiskit.providers.ibmq import least_busy


def generate_random_state(qc, pos):
    psi = random_state(1)

    init_gate = Initialize(psi)
    init_gate.label = "init"
    inverse_init_gate = init_gate.gates_to_uncompute()

    qc.append(init_gate, [pos])
    return (init_gate, inverse_init_gate)


real_quantum_computer = True

qr = QuantumRegister(3)
crx = ClassicalRegister(1)
crz = ClassicalRegister(1)
cr_result = ClassicalRegister(1)
qc = QuantumCircuit(qr, crx, crz, cr_result)


# putting q0 in random state
init_gate, inverse_init_gate = generate_random_state(qc, 0)

# creating bell-pair
qc.barrier()
qc.h(1)
qc.cx(1, 2)

# Alice's lab
qc.barrier()
qc.cx(0, 1)


# measure q1 if 1 perform bit-flip
if(not real_quantum_computer):
    qc.measure(1, crx)

# measuring in +- basis
qc.h(0)
if(not real_quantum_computer):
    qc.measure(0, crz)

# Bob's lab
if(real_quantum_computer):
    qc.barrier()
    qc.cx(1, 2)
    qc.cz(0, 2)
else:
    qc.barrier()
    qc.x(2).c_if(crx, 1)
    qc.z(2).c_if(crz, 1)

# To check if information from q0 has teleported to q2
qc.append(inverse_init_gate, [2])
qc.measure(2, 2)


# Running Computation
if(real_quantum_computer):
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    real_backend = least_busy(provider.backends(filters=lambda b: b.configuration().n_qubits >= 3 and
                                                not b.configuration().simulator and b.status().operational == True))
    counts = execute(qc, backend=real_backend,
                     shots=8192).result().get_counts(qc)
else:
    qasm_backend = Aer.get_backend('qasm_simulator')
    counts = execute(qc, qasm_backend, shots=1024).result().get_counts(qc)

# Error Checking
if(real_quantum_computer):
    error_rate_percent = sum([counts[result] for result in counts.keys() if result[0] == '1']) \
        * 100. / sum(list(counts.values()))
    print("The experimental error rate : ", error_rate_percent, "%")

# Plotting probabilities
print(counts)
plot_histogram(counts)


# qc.draw('mpl')
