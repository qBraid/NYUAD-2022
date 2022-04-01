import boto3
from braket.aws import AwsDevice
from braket.devices import LocalSimulator
from braket.circuits import Circuit
import qubovert
import numpy as np
import networkx as nx


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

    path, cost = s.parse_results(result)


# pip install dwave-ocean-sdk
# pip install amazon-braket-ocean-plugin
# import dwave.system
# import braket.ocean_plugin


# arn = "arn:aws:braket:::device/qpu/d-wave/DW_2000Q_6"
# #arn = "arn:aws:braket:::device/qpu/d-wave/Advantage_system1"
# my_bucket = f"amazon-braket-qbraid-jobs" # the name of the bucket
# my_prefix = "tomeshteague-40gmail-2ecom" # the name of the folder in the bucket
# s3_folder = (my_bucket, my_prefix)

# shots = 10

# sampler = dwave.system.EmbeddingComposite(
#             braket.ocean_plugin.BraketDWaveSampler(s3_folder, arn)
#         )

# # response = sampler.sample_qubo(qubo.Q, num_reads=shots)
# # record = response.record

# solution = []
# for row in record.sample:
#     soln_dict = {}
#     for var, assignment in zip(response.variables, row):
#         soln_dict[var] = assignment
#     solution.append(soln_dict)

# return_data = [
#     (s, e, n) for s, e, n in zip(solution, record.energy, record.num_occurrences)
# ]

# return_recarray = np.rec.array(
#     return_data, dtype=[("solution", "O"), ("energy", "<f8"), ("num_occurrences", "<i8")]
# )

# #print(return_recarray)


# for i, res in enumerate(return_recarray):
#     print('Anneal', i+1)
#     state.print_routes(res['solution'])
#     print('\tQUBO cost:', res['energy'])
#     print()


# state.parse_results(return_recarray, dwave=True)
