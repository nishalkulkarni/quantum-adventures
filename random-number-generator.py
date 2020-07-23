from qiskit import *

backend = Aer.get_backend("qasm_simulator")

# generates random number2# between 0 and 2^lim - 1
def oneshotRandomNumber(lim):
    li = [i for i in range(lim)]
    qc = QuantumCircuit(lim, lim)
    qc.h(li)
    qc.measure(li, li)
    ans = int(list(execute(qc, backend, shots=1).result().get_counts())[0], 2)
    print("Random number between 0-"+str(pow(2, lim)-1)+" is ->", ans)

# generates random number between 0 and lim - 1
def bitwiseRandomNumber(lim):
    ans = 0
    multiplier = 1

    while(ans < lim):
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        num = int(list(execute(qc, backend, shots=1).result().get_counts())[0])
        if(ans+(num*multiplier) >= lim):
            break
        ans += num*multiplier
        multiplier <<= 1

    print("Random number between 0-"+str(lim-1)+" is ->", ans)


lim = int(input("Enter a number - "))

bitwiseRandomNumber(lim)
oneshotRandomNumber(lim)
