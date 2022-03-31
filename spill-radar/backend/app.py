import json

from flask import request, Flask, Response

from qiskit_optimization import QuadraticProgram
from qiskit import Aer
from qiskit.algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.optimizers import ADAM

PORTS = {
    "Zayed Port, Abu Dhabi": [1098.04, 870.974],
    "Mina Rashid, Dubai": [1215.77, 766.165],
    "Jebel Ali Port, Dubai": [1183.42, 799.457],
    "Mina Saqr, Ras Al Khaimah": [1305.03, 694.649],
    "Khalifa Port, Abu Dhabi": [1131.68, 830.284],
    "Port of Khasab, Oman": [1345.13, 637.928],
    "King Abdulaziz Port, KSA": [537.887, 600.937],
    "King Fahd Industrial Port, KSA": [464.149, 528.187],
    "Ras Al Khair Port, KSA": [405.934, 454.205],
    "Shuwaikh Port, Kuwait": [235.171, 206.363],
    "Shuaiba Port, Kuwait": [266.219, 248.286],
    "Doha port, Kuwait": [217.06, 201.43],
    "Port Doha, Qatar": [719, 760],
    "Hamad port, Qatar": [721.587, 798.224],
    "Al-Ruwais port, Qatar": [672.428, 644.094],
    "Port of Shahid Rajaee, Iran": [847.072, 62.0962]
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


app = Flask(__name__)


@app.route('/')
def index():
    return Response("""
    Use /qubo?size=20&x=5&y=5 to specify your request.
    See also /ports and /ships for more info.
    """, mimetype="text/plain")


@app.route("/ships")
def ships():
    return Response(json.dumps(SHIPS, indent=4), mimetype="text/json")


@app.route("/ports")
def ports():
    return Response(json.dumps(PORTS, indent=4), mimetype="text/json")


@app.route('/qubo')
def qubo_classic():
    size = request.args.get('size', type=float)
    x = request.args.get('x', type=float)
    y = request.args.get('y', type=float)
    if size is None or x is None or y is None:
        return Response('{"status": "MISSING_INPUT"}', mimetype="text/json")
    qubo = create_oil_qubo(SHIPS, (size, (x, y)))
    exact_mes = NumPyMinimumEigensolver()
    eigen_optimizer = MinimumEigenOptimizer(min_eigen_solver=exact_mes)
    solution = eigen_optimizer.solve(qubo)

    # print(solution)
    solution_json = {
        "status": solution.samples[0].status.name,
        "ships": []
    }
    for i, (ship, data) in enumerate(SHIPS.items()):
        if solution.samples[0].x[i] != 0:
            solution_json["ships"].append((ship, *data))

    return Response(json.dumps(solution_json, indent=4), mimetype="text/json")


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == '__main__':
    app.run(debug=False)
