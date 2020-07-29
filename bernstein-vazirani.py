import numpy as np
from qiskit import *
from qiskit.visualization import *
from qiskit.providers.ibmq import *


# Oracle Generator
def bv_oracle(s, n):
    oracle_qc = QuantumCircuit(n+1)
    s = s[::-1]
    for i in range(n):
        if(s[i]=="1"):
            oracle_qc.cx(i, n)

    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate

# Implement generalised Bernstein-Vazirani algorithm
def bv_algorithm(oracle, n):
    bv_circuit = QuantumCircuit(n+1, n)

    bv_circuit.x(n)
    bv_circuit.h(n)

    for i in range(n):
        bv_circuit.h(i)

    bv_circuit.append(oracle, range(n+1))

    for i in range(n):
        bv_circuit.h(i)

    for i in range(n):
        bv_circuit.measure(i, i)

    return bv_circuit


b_str = input("Enter binary string: ")
n = len(b_str)
real_quantum_computer = False

oracle_gate = bv_oracle(b_str, n)
bv_circuit = bv_algorithm(oracle_gate, n)


if real_quantum_computer:
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= (n+1) and
                                           not x.configuration().simulator and x.status().operational == True))
    results = execute(bv_circuit, backend=backend, shots=1024, optimization_level=3).result().get_counts()
else:
    qasm_backend = Aer.get_backend("qasm_simulator")
    results = execute(bv_circuit, backend=qasm_backend,
                      shots=1024).result().get_counts()

# bv_circuit.draw('mpl')
plot_histogram(results)
print(results)
