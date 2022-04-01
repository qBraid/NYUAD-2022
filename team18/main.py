# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:59:19 2022

"""

# modules we implemented
from generate_profile import generate_profile
from backend.app.compile_and_verify import compile_and_verify
from application.quantum_sat import generate_circuit

from qiskit import execute
from qiskit.test.mock import FakeAthens
from qiskit.visualization import plot_histogram

# This file is an example of how to run functions in our modules above
if __name__ == "__main__":
    # generate profile using default values
    generate_profile()

    # generate quantum circuit for the application we developed
    circ = generate_circuit()
    circ.draw()

    # compile and check the equivalence
    circ_comp, equivalent = compile_and_verify(circ)
    print('Compiled circuit is equivalent to original circuit:', equivalent)

    # simulate the original circuit
    job = execute(circ_comp, shots=1000, backend=FakeAthens())
    result = job.result()
    counts = result.get_counts(circ_comp)
    plot_histogram(counts, filename='backend/images/hist_compiled.png')

    # verify using default values
    circ_comp_error, equivalent = compile_and_verify(circ, introduce_error=True)
    print('Compiled circuit is equivalent to original circuit:', equivalent)

    # simulate the original circuit
    job = execute(circ_comp_error, shots=1000, backend=FakeAthens())
    result = job.result()
    counts = result.get_counts(circ_comp_error)
    plot_histogram(counts, filename='backend/images/hist_compiled_error.png')