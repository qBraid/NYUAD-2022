# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:59:19 2022

"""

# modules we implemented
from generate_profile import generate_profile
from compile_and_verify import compile_and_verify
from application.quantum_sat import generate_circuit

# This file is an example of how to run functions in our modules above
if __name__ == "__main__":
    # generate profile using default values
    generate_profile()

    # generate quantum circuit for the application we developed
    circ = generate_circuit()
    circ.draw()

    # compile and check the equivalence
    circ_comp, equivalent = compile_and_verify(circ)
    print(equivalent)

    # verify using default values
    circ_comp_error, equivalent = compile_and_verify(circ, introduce_error=True)
    print(equivalent)
