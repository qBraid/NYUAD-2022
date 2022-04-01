# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 20:00:08 2022
    
"""
from qiskit import QuantumCircuit, transpile
import numpy as np
import random
import os

# single qubit gates with no parameters
single_qubit_gates_no_params = ["x", "y", "z", "h", "s", "sdg", "t", "tdg", "sx", "sxdg"]

# single qubit gates with no parameters
single_qubit_gates_1_params = ["p", "rx", "ry", "rz"]

# single qubit gates with 2 parameters
single_qubit_gates_2_params = ["u2"]

# single qubit gates with 3 parameters
single_qubit_gates_3_params = ["u3"]

# single qubit gates with 3 parameters
two_qubit_gates = ["swap", "iswap"]

# path to the profile directory
cd = "profiles/"


# create gate (with params) and return it
def create_gate_with_params(circuit, gate, number_qubits, number_params):
	if number_qubits == 1:
		param_list = []

		for i in range(number_params):
			param_list.append(random.uniform(-np.pi, np.pi))

		getattr(circuit, gate)(*param_list, 0)
	elif number_qubits == 2:
		getattr(circuit, gate)(0, 1)

	return circuit


# return gate with number of controls
def create_controlled_gate(circuit, controls, number_qubits):
	# convert circuit to gate and add number of controls
	custom_circuit = circuit.to_gate().control(controls)

	# create new circuit with number of qubits for gate + for controls
	circuit_with_controls = QuantumCircuit(controls + number_qubits)

	# append gate with controls to circuit with controls
	# second argument is a range for number of controls
	circuit_with_controls.append(custom_circuit, range(controls + number_qubits))

	return circuit_with_controls


# create look up table for set of gates
# with different amounts of controls
def create_lookup_table(gates, basis_gates, number_qubits, number_params, max_controls, optimization_level, cd):
	gate_stats = []
	# iterate through each gate
	for gate in gates:

		# create circuit with all amount of controls
		for controls in range(0, max_controls + 1):

			# create single qubit circuit
			circuit = QuantumCircuit(number_qubits)

			# create gate with its params
			circuit = create_gate_with_params(circuit, gate, number_qubits, number_params)

			# if there are controls,
			# create circuit with controls
			if controls != 0:
				circuit_with_controls = create_controlled_gate(circuit, controls, number_qubits)

				# set circuit that will be transpiled to the circuit with controls
				circuit = circuit_with_controls

			# transpile the circuit
			transpiled_circuit = transpile(circuit, basis_gates=basis_gates, optimization_level=optimization_level)
			gate_stats.append([gate, controls, transpiled_circuit.size()])

	# creating a txt file with name "gate_status_op_lv_n.txt", n being the optimization level
	f = open(cd + "gate_stats_op_lv_" + str(optimization_level) + ".txt", "a")

	# writing the information from gate_stats list to the text file
	for i in np.arange(len(gate_stats)):
		f.writelines([gate_stats[i][0], " ", str(gate_stats[i][1]), " ", str(gate_stats[i][2])])
		f.writelines(['\n'])

	f.close()


# remove all previous profiles
def remove_profile(directory, optimization_level):
	files = os.listdir(directory)
	for item in files:
		if item == ("gate_stats_op_lv_" + str(optimization_level) + ".txt"):
			os.remove(os.path.join(directory, item))
			# print("successfully removed: ", item)


# generate profile for different optimization levels
def generate_profile(optimization_level: int = 1, max_contols: int = 5, basis_gates=None):
	# remove previous profile with this optimization_level
	if basis_gates is None:
		basis_gates = ['id', 'rz', 'sx', 'x', 'cx']
	remove_profile(cd, optimization_level)

	# execution of create_lookup table function for all possible gates in IBM Qiskit
	create_lookup_table(single_qubit_gates_no_params, basis_gates, 1, 0, max_contols, optimization_level, cd)
	create_lookup_table(single_qubit_gates_1_params, basis_gates, 1, 1, max_contols, optimization_level, cd)
	create_lookup_table(single_qubit_gates_2_params, basis_gates, 1, 2, max_contols, optimization_level, cd)
	create_lookup_table(single_qubit_gates_3_params, basis_gates, 1, 3, max_contols, optimization_level, cd)
	create_lookup_table(two_qubit_gates, basis_gates, 2, 0, max_contols, optimization_level, cd)
