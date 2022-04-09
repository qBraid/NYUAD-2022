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
    print('Generating profile for verification ...')
    generate_profile()
    print('... generated profile')

    # generate quantum circuit for the application we developed
    print('Generating application circuit ...')
    circ = generate_circuit()
    print('... generated application circuit')

    # compile and check the equivalence
    print('Compiling and verifying the circuit ...')
    circ_comp, equivalent = compile_and_verify(circ)
    print('... compiled circuit is equivalent to original circuit:', equivalent)

    # simulate the original circuit
    print('Simulating the resulting circuit and saving histogram ...')
    job = execute(circ_comp, shots=1000, backend=FakeAthens())
    result = job.result()
    counts = result.get_counts(circ_comp)
    plot_histogram(counts, filename='images/hist_compiled.png')
    print('... done')

    # verify using default values
    print('Compiling and verifying the circuit and introducing an error ...')
    circ_comp_error, equivalent = compile_and_verify(circ, introduce_error=True)
    print('... compiled circuit is equivalent to original circuit:', equivalent)

    # simulate the original circuit
    print('Simulating the resulting circuit and saving histogram ...')
    job = execute(circ_comp_error, shots=1000, backend=FakeAthens())
    result = job.result()
    counts = result.get_counts(circ_comp_error)
    plot_histogram(counts, filename='images/hist_compiled_error.png')
    print('... done')
