import os
from qubo_helper import Qubo
from tsp_problem import TSPProblem 
from vrp_problem import VRPProblem
from vrptw_problem import VRPTWProblem
from vrptw_solvers import *
from vrp_solvers import *
from itertools import product
import DWaveSolvers
import networkx as nx
import numpy as np
from input import *

CAPACITY = 1000

class MainSolver:
    def __init__(self, scenario_text, graph_text):

        print(scenario_text)
        print(graph_text)
        
        test, dijkstra_paths = read_full_test(scenario_text, graph_text, time_windows = False)

        # Problem parameters
        sources = test["sources"]
        costs = test["costs"]
        time_costs = test["time_costs"]
        capacities = test["capacities"]
        dests = test["dests"]
        weigths = test["weights"]
        time_windows = test["time_windows"]

        only_one_const = 10000000.
        order_const = 1.
        capacity_const = 0. # Not used in this example
        time_const = 0. # not used in this example

        problem = VRPProblem(sources, costs, time_costs, capacities, dests, weigths)
        solver = SolutionPartitioningSolver(problem, FullQuboSolver(problem))
        result = solver.solve(only_one_const, order_const, capacity_const,
                solver_type = 'braket', num_reads = 500)
        if not result:
            result.solution = [[], []]

        print(result.solution)
        self.value = result.solution
        
    def return_value(self):
        return self.value
