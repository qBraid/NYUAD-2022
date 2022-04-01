# CVRP approach using quantum computing

*Note* : This code is based on : https://github.com/xBorox1/D-Wave-Leap---CVRP


Few quantum approaches for CVRP problems. It isn't fully ended version and it's not well described. If you want to use it, I recommend you to change only file paths in main. I want to improve code and approaches and then create more user-friendly version. Also you need to configure D-Wave Leap first.

## API Usage

* Prepare test scenario according to Input specification.
* Read the test by function read_full_test or read_test.

## Input specification

You need to prepare 2 files :

* Graph file in simple csv format, named vertex_weights.csv, containing 3 columns as edges: id of first vertex, id of second vertex and weight of edge. Graph is directed.
* Scenario text file. Format is described in 'example_scenario'.

## Running
* Use python3.7.9
* Choose a solver.
* Read test by read_test function or read_full_test from input.py.
* Run solve function from solver in same way as in main.

## Available solvers :

* FullQuboSolver - solving VRP problem only by quantum annealing, working for small cases
* AveragePartitionSolver - improved version of previous one, but using only qunatum annealing, working for small cases and only for VRP
* DBScanSolver - hybrid algorithm for VRP and CVRP with equal capacities, working for bigger cases, based on https://arxiv.org/abs/1812.02300
* SolutionPartitioningSolver - hybrid algorithm for CVRP, working for cases with 200 deliveries if used with DBScanSolver. (as parameter - example in main)
