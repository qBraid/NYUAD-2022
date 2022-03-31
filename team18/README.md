# NYUAD Hackathon for social good in the arab world
## Team 18 - Verified Compilation of Quantum Circuits

### People

 - Lukas Burgholzer (Mentor), Johannes Kepler University Linz, Austria
 - Geon Tack Lee (Hacker), New York University Abu Dhabi, UAE
 - Feel free to add yourself here

### Getting started

Clone this repository
```console 
git clone https://github.com/burgholzer/NYUAD-2022
```
Our team's contribution is supposed to go into the `team18` folder. So move there
```console
cd NYUAD-2022/team18
```
A minimum working example can be found in the `main.py` file.
It shows how to use the MQT QCEC tool to verify that a very simple circuit has been correctly compiled to the 5-qubit IBMQ Athens architecture. 
To get this working, create and activate a new virtual environment for the project:
```console
python3 -m venv venv
. venv/bin/activate
```
Install the requirements from the `requirements.txt` file:
```console 
pip install -r team18/requirements.txt
```
Then execute the Python script
```console 
python3 team18/main.py
```

### Designing an efficient strategy
In order to determine an efficient strategy, a lookup table can be created from the information gathered from the IBM Qiskit quantum circuit compilation flow.

To this end, the following high-level operations shall be supported:
 - **single-qubit** gates: 
   - "i", "id", "iden": identity gate
   - "x", "y", "z": Pauli operations
   - "h": Hadamard gate
   - "s", "sdg", "t", "tdg": Phase gates
   - "sx", "sxdg": sqrt-X gate (and inverse)

 - **two-qubit** gates: 
   - "swap"
   - "iswap"

There are some parametrized gates (single-qubit rotations) that need some extra care:
 - "p": arbitrary angle phase gate (generalization of Z, S, T)
 - "rx", "ry", "rz": arbitrary rotations around the X, Y, or Z axis
 - "u2": general rotation specified by two parameters
 - "u", "u3": general rotation specified by three parameters
For these gates, it is probably best to just choose parameter values at random when determining the corresponding compilation cost.

In addtion, all of the above gates (except for the identity gate) can have arbitrarily many control qubits attached to them, e.g., 
 - "cx": controlled-X or CNOT operation
 - "ccx" controlled-controlled-X or Toffoli gate
 - ...

Typically, there are multiple ways of realizing gates with more than 2 controls. Qiskit offers three different options for that:
 - `mode='noancilla'`
 - `mode='recursion'`
 - `mode='v-chain'`

There should be a different profile for each of these options.
Furthermore, there should be a different profile for each optimization level of the IBM Qiskit compiler (O0 -- O3)

The target gate-set for compilation should be an argument of the function that computes the decomposition costs.
In general, you will be targeting the IBM gate-set consisting of `["id", "rz", "sx", "x", "cx"]`.
