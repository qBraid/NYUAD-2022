# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:59:19 2022

"""
from qiskit import QuantumCircuit, transpile, Aer, IBMQ
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from qiskit.providers.aer import QasmSimulator
import numpy as np
from math import pi, sqrt
import random
import sys
import os
from qiskit.test.mock import FakeAthens
from mqt import qcec

# modules we implemented
from generate_profile import generate_profile
from verify_circuit import verify_circuit 

### This file is an example of how to run functions in our modules above

##### !!! THIS IS ONLY RUN ONCE !!! ###
# generate profile using default values
for i in range(4):
    generate_profile(optimization_level=i)

# TEST CASE CIRCUIT
# original circuit, arbitrary
circ = QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(0, 2)
circ.ccx(0, 2, 1)
circ.measure_all()

# verify using default values
result = verify_circuit(circ)
print(result)







