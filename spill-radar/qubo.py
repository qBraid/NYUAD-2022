import argparse
import json

from qiskit_optimization import QuadraticProgram
from qiskit import BasicAer, Aer
from qiskit.algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.optimizers import COBYLA, SLSQP, ADAM


parser = argparse.ArgumentParser()
parser.add_argument("size", help="Size of the oil spill", type=int)
parser.add_argument("x", help="x coordinates of the oil spill", type=int)
parser.add_argument("y", help="y coordinates of the oil spill", type=int)
parser.add_argument("--quantum", help="use quantum to solve", action="store_true")
args = parser.parse_args()

PORTS = {
    "Zayed Port, Abu Dhabi": [763, 278],
    "Mina Rashid, Dubai": [854, 363],
    "Jebel Ali Port, Dubai": [829, 336],
    "Mina Saqr, Ras Al Khaimah": [923, 421],
    "Khalifa Port, Abu Dhabi": [789, 311],
    "Port of Khasab, Oman": [954, 467],
    "King Abdulaziz Port, KSA": [330, 497],
    "King Fahd Industrial Port, KSA": [273, 556],
    "Ras Al Khair Port, KSA": [228, 616],
    "Shuwaikh Port, Kuwait": [96, 817],
    "Shuaiba Port, Kuwait": [120, 783],
    "Doha port, Kuwait": [82, 821],
    "Port Doha, Qatar": [470, 368],
    "Hamad port, Qatar": [472, 337],
    "Al-Ruwais port, Qatar": [434, 462],
    "Port of Shahid Rajaee, Iran": [569, 934]
}

SHIPS = {
    "ship1": (5, PORTS ["Zayed Port, Abu Dhabi"]),
    "ship2": (10, PORTS ["Mina Rashid, Dubai"]),
    "ship3": (5, PORTS ["Jebel Ali Port, Dubai"]),
    # "ship4": (10, PORTS ["Mina Saqr, Ras Al Khaimah"]),
    # "ship5": (5, PORTS ["Khalifa Port, Abu Dhabi"]),
    # "ship6": (10, PORTS ["Port of Khasab, Oman"]),
    # "ship7": (10, PORTS ["King Abdulaziz Port, KSA"]),
    # "ship8": (10, PORTS ["King Fahd Industrial Port, KSA"]),
    # "ship9": (10, PORTS ["Ras Al Khair Port, KSA"]),
    # "ship10": (10, PORTS ["Shuwaikh Port, Kuwait"]),
    # "ship11": (10, PORTS ["Shuaiba Port, Kuwait"]),
    # "ship12": (10, PORTS ["Doha port, Kuwait"])
}

# oilspill = (size, coordinates)
oilspill = (args.size, (args.x, args.y))


def create_oil_qubo(ships, oilspill):
    mod = QuadraticProgram("oil spill")# create a binary variable for each ship indicating whether we should send it or not
    for ship in ships.keys():
        mod.binary_var(name=ship)
# add the distance between each ship and the oilspill
    kilometers = {}
    for ship, data in ships.items():
        kilometers[ship] = ((data[1][0] - oilspill[1][0]) **2 + (data[1][1] - oilspill[1][1]) **2)**(0.5)
    mod.minimize(linear=kilometers)
#the capabilities and oil spill size as linear constraint
    capabilities = {}
    for ship, data in ships.items():
        capabilities[ship] = data[0]
    mod.linear_constraint(linear=capabilities, sense=">=", rhs=oilspill[0], name="lin_eq")
    return mod

qubo = create_oil_qubo(SHIPS, oilspill)
print(qubo.export_as_lp_string())

if args.quantum:
    backend = Aer.get_backend('statevector_simulator')
    qaoa = QAOA(optimizer=ADAM(), quantum_instance=backend, reps=1)
    eigen_optimizer = MinimumEigenOptimizer(min_eigen_solver=qaoa)
    solution = eigen_optimizer.solve(qubo)
else:
    exact_mes = NumPyMinimumEigensolver()
    eigen_optimizer = MinimumEigenOptimizer(min_eigen_solver=exact_mes)
    solution = eigen_optimizer.solve(qubo)

#print(solution)
solution_json = {
    "status": solution.samples[0].status.name,
    "ships": []
}
for i, ship in enumerate(SHIPS):
    if solution.samples[0].x[i] != 0:
        solution_json["ships"].append(ship)

#print(json.dumps(solution_json, indent=4))
