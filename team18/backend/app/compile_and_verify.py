# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:59:59 2022

"""
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import XGate
from qiskit.test.mock import FakeAthens, FakeBackend
from mqt import qcec


# verification
def compile_and_verify(circuit_original: QuantumCircuit, backend: FakeBackend = FakeAthens(), optimization_level: int = 1,
                       introduce_error: bool = False):

    # compile according to specified optimization level
    circ_comp = transpile(circuit_original, backend=backend, optimization_level=optimization_level)

    if introduce_error:
        error = QuantumCircuit(circ_comp.num_qubits)
        error.x(0)
        circ_comp = error + circ_comp

    # initialize the equivalence checker
    ecm = qcec.EquivalenceCheckingManager(circuit_original, circ_comp)

    # set the application scheme to be based off a profile
    ecm.set_application_scheme('gate_cost')
    ecm.set_gate_cost_profile('profiles/gate_stats_op_lv_' + str(optimization_level) + '.txt')

    # execute the check
    ecm.run()

    # obtain the result
    considered_equivalent = ecm.get_results().considered_equivalent()

    return circ_comp, considered_equivalent
