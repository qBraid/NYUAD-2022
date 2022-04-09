import os

from qiskit import *
from qiskit.circuit.library import PhaseOracle


def generate_oracle():
    filename = "3sat.dimacs"
    dimacs_specification = "c example DIMACS CNF 3-SAT\n" \
        "p cnf 3 3\n" \
        "1 2 -3 0\n" \
        "-1 2 -3 0\n" \
        "-1 -2 -3 0\n"
    with open(filename, "wt") as file:
        file.write(dimacs_specification)
        file.close()

    oracle = PhaseOracle.from_dimacs_file(filename)
    os.remove(filename)
    oracle.name = "$U_\omega$"
    return oracle


def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits - 1)
    qc.mct(list(range(nqubits - 1)), nqubits - 1)  # multi-controlled-toffoli
    qc.h(nqubits - 1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    u_s = qc.to_gate()
    u_s.name = "$U_s$"
    return u_s


def initialize_s(qc, qubits):
    """Apply a H-gate to 'qubits' in qc"""
    for q in qubits:
        qc.h(q)
    return qc


def generate_circuit():
    nqubits = 3
    grover_circuit = QuantumCircuit(nqubits)
    grover_circuit = initialize_s(grover_circuit, range(nqubits))
    grover_circuit.append(generate_oracle(), range(nqubits))
    grover_circuit.append(diffuser(nqubits), range(nqubits))
    grover_circuit.measure_all()
    return grover_circuit


if __name__ == "__main__":
    qc = generate_circuit()
    print(qc.draw())
