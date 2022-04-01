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
        # Solomon
        #GRAPH = '../graphs/50/' + str(t) + '.csv'
        #TEST = '../solomon/50/' + str(t) + '.test'
        #test = read_full_test(TEST, GRAPH, solomon = True)

        # Bruxelles
        #TEST = '../tests_cvrptw/exact/' + t + '.test'
        #test = read_test(TEST)

        # Christofides_79
        #GRAPH = '../tests_cvrp/christofides-1979_graphs/CMT' + str(t) + '_medium.csv'
        #TEST = '../tests_cvrp/christofides-1979_GLAD/CMT' + str(t) + '_medium.test'
        
        test, dijkstra_paths = read_full_test(scenario_text, graph_text, time_windows = False)

        # Christofides_69
        #GRAPH = '../tests_cvrp/christofides-1969_graphs/' + str(t) + '.csv'
        #TEST = '../tests_cvrp/christofides-1969_GLAD/' + str(t) + '.test'
        #test = read_full_test(TEST, GRAPH, time_windows = False)

        # Problem parameters
        sources = test['sources']
        costs = test['costs']
        time_costs = test['time_costs']
        capacities = test['capacities']
        dests = test['dests']
        weigths = test['weights']
        time_windows = test['time_windows']

        only_one_const = 10000000.
        order_const = 1.
        capacity_const = 0. #not important in this example
        time_const = 0. #not important in this example

        problem = VRPProblem(sources, costs, time_costs, capacities, dests, weigths)
        #solver = FullQuboSolver(problem)
        # solver = SolutionPartitioningSolver(problem, DBScanSolver(problem, anti_noiser = False, MAX_LEN = 10))
        solver = SolutionPartitioningSolver(problem, FullQuboSolver(problem))

        #problem = VRPTWProblem(sources, costs, time_costs, capacities, dests, weigths, time_windows)
        #vrp_solver = SolutionPartitioningSolver(problem, DBScanSolver(problem, anti_noiser = False))
        #solver = MergingTimeWindowsVRPTWSolver(problem, vrp_solver)

        #result = solver.solve(only_one_const, order_const, capacity_const,
        #        solver_type = 'qbsolv', num_reads = 500)

        result = solver.solve(only_one_const, order_const, capacity_const,
                solver_type = 'braket', num_reads = 500)
        if result == None:
            result.solution = [[], []]

        print(result.solution)

        
        self.value = result.solution
        
    def return_value(self):
        return self.value
