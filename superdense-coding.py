from qiskit import *
from qiskit.visualization import *
from qiskit.providers.ibmq import least_busy


def encode_message(qc, qubit, msg):
    if(msg == "00"):
        pass
    elif(msg == "10"):
        qc.x(qubit)
    elif(msg == "01"):
        qc.z(qubit)
    elif(msg == "11"):
        qc.z(qubit)
        qc.x(qubit)
    else:
        print("Invalid Message: Sending '00'")


def decode_message(qc, a, b):
    qc.cx(a, b)
    qc.h(a)


real_quantum_computer = True

qc = QuantumCircuit(2)

# Create bell-pair
qc.h(0)
qc.cx(0, 1)
qc.barrier()

# Input & Encode message [Alice's Lab]
message = input("Enter 2 bit binary number - ")
encode_message(qc, 0, message)
qc.barrier()

# Decode message [Bob's Lab]
decode_message(qc, 0, 1)
qc.barrier()

qc.measure_all()

if(real_quantum_computer):
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 2
                                           and not x.configuration().simulator
                                           and x.status().operational == True))
    result = execute(qc, backend=backend, shots=1024).result().get_counts(qc)
else:
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=1024).result().get_counts(qc)

# Print Result
print(result)
plot_histogram(result)

# Print Accuracy
accuracy = (result[message]/1024)*100
print("Accuracy = %.2f%%" % accuracy)

qc.draw('mpl')
