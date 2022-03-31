# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:59:59 2022

"""
from qiskit import QuantumCircuit, transpile, Aer, IBMQ
from qiskit.test.mock import FakeAthens
from mqt import qcec


# verification
def verify_circuit(circuit_original, backend=FakeAthens(), optimization_level=1):
    
    # compile according to specified optimization level
    circ_comp = transpile(circuit_original, backend=backend, optimization_level=optimization_level)
    
    original_pic = circuit_original.draw(fold=-1, filename="images/original_pic.png")
    compiled_pic = circ_comp.draw(fold=-1, filename="images/compiled_pic.png")
    
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
