import boto3
from braket.aws import AwsDevice
from braket.devices import LocalSimulator
from braket.circuits import Circuit
import qubovert
import numpy as np
import networkx as nx
from flask import Flask, request

app = Flask(__name__)

app.debug = True


class VRPstate:
    def __init__(self, G, num_vehicles):
        self.num_nodes = len(G.nodes)
        self.num_vehicles = num_vehicles
        self.G = G  # depot is always node 0
        self.vehicle_locations = [0 for _ in range(self.num_vehicles)]
        self.vehicle_routes = [[] for _ in range(self.num_vehicles)]
        self.visited_nodes = [0 for _ in range(self.num_nodes)]

        self.qubo = None
        self.C = None

    def get_cost_matrix(self):
        C = np.zeros((self.num_nodes, self.num_nodes))
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                if self.G.has_edge(i, j):  # edge exists
                    C[i, j] = self.G[i][j]['weight']
                    C[j, i] = C[i, j]
                else:  # edge doesnt exist
                    path = nx.shortest_path(
                        self.G, source=i, target=j, weight='weight')
                    C[i, j] = sum([self.G[path[i]][path[i+1]]['weight']
                                  for i in range(len(path)-1)]) * 10 * 3**len(path)
                    C[j, i] = C[i, j]
        self.C = C

    def A_func(self, A_2, binary_vars):
        for i in range(len(binary_vars)):
            for j in range(i+1, len(binary_vars)):
                self.qubo[(binary_vars[i], binary_vars[j])] += A_2 * 2

        for var in binary_vars:
            self.qubo[(var,)] -= A_2 * 1

    def add_constraints(self, A_2):
        # Ensure each node is visited by a single vehicle
        for k in range(self.num_nodes):
            binary_vars = []
            for vehicle in range(self.num_vehicles):
                for timestep in range(self.num_nodes):
                    binary_vars.append((vehicle, k, timestep))
            self.A_func(A_2, binary_vars)

        # Each vehicle is in one location at one time
        for vehicle in range(self.num_vehicles):
            for timestep in range(self.num_nodes):
                binary_vars = [(vehicle, n, timestep)
                               for n in range(self.num_nodes)]
                self.A_func(A_2, binary_vars)

        # Each vehicle is in its current location at time t=0
        for m in range(self.num_vehicles):
            for n in range(self.num_nodes):
                if self.vehicle_locations[m] == n:
                    self.qubo[((m, n, 0),)] -= A_2
                else:
                    self.qubo[((m, n, 0),)] += A_2

    def get_qubo(self, A_1=1, A_2=1000):
        self.get_cost_matrix()
        self.qubo = qubovert.QUBO()

        # first order terms
        for i in range(self.num_vehicles):
            for j in range(1, self.num_nodes):
                # returning to depot cost
                self.qubo[((i, j, self.num_nodes),)] += A_1 * self.C[j, 0]

        for m in range(self.num_vehicles):
            for n in range(self.num_nodes):
                # travelling from current position cost
                self.qubo[((m, n, 1),)] += A_1 * \
                    self.C[n, self.vehicle_locations[m]]

        # second order terms
        for m in range(self.num_vehicles):
            for n in range(1, self.num_nodes):
                for i in range(self.num_nodes):
                    for j in range(self.num_nodes):
                        # Add second order term to qubo
                        self.qubo[((m, i, n), (m, j, n+1))
                                  ] += A_1 * self.C[i, j]

        # Add constraint term Q
        self.add_constraints(A_2)

        return self.qubo

    def print_routes(self, best_state):
        for vehicle in range(self.num_vehicles):
            total_cost = 0
            print(f'Vehicle {vehicle}:')
            cur_path = sorted([key for key, val in best_state.items(
            ) if val == 1 and key[0] == vehicle], key=lambda v: v[2])
            print(f'\t{self.vehicle_locations[vehicle]} --> ', end='')
            prev_stop = self.vehicle_locations[vehicle]
            for stop in cur_path:
                total_cost += self.C[prev_stop, stop[1]]
                prev_stop = stop[1]
                print(f'{stop[1]} --> ', end='')
            print('END')

            # total cost
            print('\t Total Cost =', total_cost)

    def parse_results(self, result, dwave=False):
        """
        NOTE: this function assumes num_vehicles = 1

        Walk through the paths returned by the QUBO solver,
        remove duplicates, and compute the cost of the pruned path.
        """
        all_paths = []
        for res in result:
            pruned_path = []
            for vehicle in range(self.num_vehicles):
                total_cost = 0
                if dwave:
                    solution = res['solution']
                else:
                    solution = res.state
                cur_path = sorted([key for key, val in solution.items(
                ) if val == 1 and key[0] == vehicle], key=lambda v: v[2])
                prev_stop = self.vehicle_locations[vehicle]
                for stop in cur_path:
                    if not stop[1] in pruned_path:
                        pruned_path.append(stop[1])
                        total_cost += self.C[prev_stop, stop[1]]
                        prev_stop = stop[1]

            for node in self.G.nodes:
                if not node in pruned_path:
                    pruned_path.append(node)

            all_paths.append((pruned_path, total_cost))

        return sorted(all_paths, key=lambda v: v[1])[0]

 
def generateGraph(edge_list):
    G = nx.Graph()
    G.add_edges_from(edge_list)
    return G


def wrapper(edge_list):
    G = generateGraph(edge_list)
    s = VRPstate(G, 1)

    qubo = s.get_qubo()

    result = qubovert.sim.anneal_qubo(
        qubo.Q, num_anneals=4, anneal_duration=int(1e6))

    return s.parse_results(result)


graph = [[0,1,{ 'weight':7159.410860493759}],[0,2,{ 'weight':233.94604044176444}],[0,3,{ 'weight':3890.5286652701484}],[0,4,{ 'weight':4703.793914383512}],[0,5,{ 'weight':5561.165303906478}],[0,6,{ 'weight':3967.7741322172005}],[0,7,{ 'weight':8722.006472181123}],[1,2,{ 'weight':6970.920516041224}],[1,3,{ 'weight':6044.741521831752}],[1,4,{ 'weight':7664.247010457612}],[1,5,{ 'weight':1666.9607728278909}],[1,6,{ 'weight':4886.368473714739}],[1,7,{ 'weight':6990.199597282921}],[2,3,{ 'weight':3674.389079831615}],[2,4,{ 'weight':4531.737631816009}],[2,5,{ 'weight':5363.002121826112}],[2,6,{ 'weight':3734.7205936745318}],[2,7,{ 'weight':8496.588845476057}],[3,4,{ 'weight':1684.0320296982757}],[3,5,{ 'weight':4494.18361875633}],[3,6,{ 'weight':1162.2516632969364}],[3,7,{ 'weight':4876.677819061241}],[4,5,{ 'weight':6154.675863099172}],[4,6,{ 'weight':2826.472730888577}],[4,7,{ 'weight':4968.2289191662285}],[5,6,{ 'weight':3333.4508779435923}],[5,7,{ 'weight':6368.629368343863}],[6,7,{ 'weight':4873.57496985432}]]


markers = [[24.46994245833937, 54.3871], [24.4206036116, 54.3416592737], [24.4694245833937, 54.384859571], [24.4745537206036116, 54.348993416592737], [24.4894245833937, 54.34584229259571], [24.434137206036116, 54.3487416592737], [24.464114245833937, 54.3484229259571], [24.47137206036116, 54.30093416592737]] 

print(graph)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/qc") 
def qc():
    return {}

@app.route("/api/graph", methods=["GET", "POST"])
def handle_graph():
    global graph
    # print(graph)
    if request.method == "GET":
        return {"graph": graph}
    if request.method == "POST":
        graph = request.get_json().get("graph")
        print(graph)
        return {"ok": True} 

@app.route("/api/markers", methods=["GET", "POST"])
def handle_markers():
    global markers
    if request.method == "GET":
        return {"markers": markers}
    if request.method == "POST":
        marker = request.get_json().get("marker")
        markers.append(marker)
        return {"ok": True}

@app.route("/test", methods=["GET"])
def test_post():
    global graph
    return {"path": wrapper(graph)}

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5050)