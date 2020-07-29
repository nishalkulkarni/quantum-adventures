import numpy as np
from qiskit import *
from qiskit.visualization import *
from qiskit.providers.ibmq import *


# Oracle Generator
def dj_oracle(case, n):
    oracle_qc = QuantumCircuit(n+1)

    if case == "balanced":
        b_str = format(np.random.randint(1, 2**n), '0'+str(n)+'b')

        for i in range(len(b_str)):
            if b_str[i] == '1':
                oracle_qc.x(i)

        for i in range(n):
            oracle_qc.cx(i, n)

        for i in range(len(b_str)):
            if b_str[i] == '1':
                oracle_qc.x(i)
    elif case == "constant":
        if np.random.randint(2) == 1:
            oracle_qc.x(n)

    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate

# Implement generalised Deutsch-Jozsa algorithm
def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n+1, n)

    dj_circuit.x(n)
    dj_circuit.h(n)

    for i in range(n):
        dj_circuit.h(i)

    dj_circuit.append(oracle, range(n+1))

    for i in range(n):
        dj_circuit.h(i)

    for i in range(n):
        dj_circuit.measure(i, i)

    return dj_circuit


n = 4
real_quantum_computer = False

oracle_gate = dj_oracle('balanced', n)
dj_circuit = dj_algorithm(oracle_gate, n)
dj_circuit.draw()

if real_quantum_computer:
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= (n+1) and
                                           not x.configuration().simulator and x.status().operational == True))
    results = execute(dj_circuit, backend=backend, shots=1024, optimization_level=3).result().get_counts()
else:
    qasm_backend = Aer.get_backend("qasm_simulator")
    results = execute(dj_circuit, backend=qasm_backend,
                      shots=1024).result().get_counts()

print(results)
# plot_histogram(results)
