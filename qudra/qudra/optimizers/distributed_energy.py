"""
DistributedEnergyOptimizer
"""

from typing import Dict, List, Tuple, Any, Optional

from braket.ocean_plugin import BraketDWaveSampler
from dwave.system.composites import EmbeddingComposite
from matplotlib import rcParams
from qiskit import Aer
from qiskit.algorithms import QAOA, VQE, NumPyMinimumEigensolver
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer, GroverOptimizer

import dimod
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def gen_transportation_losses(
    distances: List[float],
) -> List[Tuple[float, float, float]]:
    """
    Generate Transportation Losses

    This is an example for how one may generate transportation losses.

    start-up cost:          Ai = 0
    linear ramp-up cost:    Bi = distance_i/avg_distance
    quadratic ramp-up cost: Ci = (distance_i - avg_distance)/std_distance

    Args:
        distances (List[float]):
            Distances of plants from the center of a city/state/country.
            This list has n elements, where n is the number of plants.

    Returns:
        cost (List[Tuple[float,float,float]]):
            List of transportation loss related costs for each plant.
            Each element has the form (Ai, Bi, Ci) as described above.
            This list has n elements, where n is the number of plants.
    """
    n = len(distances)
    avg_distance = np.mean(distances)
    std_distance = np.std(distances)
    cost: List[Tuple[float, float, float]] = []
    for i in range(n):
        cost.append(
            (
                0.0,  # Ai
                distances[i] / avg_distance,  # Bi
                (distances[i] - avg_distance) / std_distance,  # Ci
            )
        )
    return cost


def gen_params_multicost(
    cost_types: Dict[str, List[Tuple[float, float, float]]],
    weights: Dict[str, float],
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate model parameters

    Args:
        cost_type (dict):
            key (str): e.g. CO2 emissions
            val (list[tuple(float,float,float)]): [(A, B, C),...]
            e.g.:
                cost_types = {
                    "CO2": [(A1,B1,C1),(A2,B2,C2),(A3,B3,C3)],
                    "Efficiency": [(A1,B1,C1),(A2,B2,C2),(A3,B3,C3)],
                    "Transportation Loss": [(A1,B1,C1),(A2,B2,C2),(A3,B3,C3)],
                }

    Returns:
        params (dict):
            key (str): parameter name
            val (Any): usually float or list or something of the like

    """

    params = params if params is not None else {}

    params["n"] = params.get("n", len(list(cost_types.values())[0]))
    params["A"] = [0 for _ in range(params["n"])]
    params["B"] = [0 for _ in range(params["n"])]
    params["C"] = [0 for _ in range(params["n"])]

    for cost_type, costs in cost_types.items():
        for plant_indx in range(params["n"]):
            params["A"][plant_indx] += weights[cost_type] * costs[plant_indx][0]
            params["B"][plant_indx] += weights[cost_type] * costs[plant_indx][1]
            params["C"][plant_indx] += weights[cost_type] * costs[plant_indx][2]

    return params


class DistributedEnergyOptimizerResults:
    def __init__(self, results: Any, extras: Optional[Dict[str, Any]] = None) -> None:
        """
        Creates DistributedEnergyOptimizerResults object.

        Args:
            results (Any):
                results object produced by optimization problem
            extras (Dict[str, Any]):
                key (str): extra label
                val (Any): extra value
        """
        self._results: Any = results
        self._extras: Dict[str, Any] = extras if extras is not None else {}

    @property
    def results(self) -> Any:
        return self._results

    @property
    def extras(self) -> Dict[str, Any]:
        return self._extras


class DistributedEnergyOptimizer:
    """
    Optimizing unit commitment from a distributed energy network.

    The optimizer has been adapted from the work in:
        Akshay Ajagekar and Fengqi You. Quantum computing for energy
        systems optimization: Challenges and opportunities. Energy 179 (2019).
        https://doi.org/10.1016/j.energy.2019.04.186
    """

    REQUIRED_PARAMS = ["A", "B", "C", "P_min", "P_max", "L", "N"]

    def __init__(self, params) -> None:
        """
        Set up DistributedEnergyOptimizer object.

        Args:
            params (dict): required params specificed by REQUIRED_PARAMS
                key (str): param name
                val (Any): param values
        """

        for label in self.REQUIRED_PARAMS:  # make sure we have all the required params
            if label not in params:
                raise ValueError(f"Please provide {label} in params.")

        self.params = params.copy()
        self.params["alpha"] = params.get("alpha", 5e5)
        self.params["beta"] = params.get("beta", 8)
        self.params["n"] = len(self.params["A"])

        self.params["plant_names"] = params.get(
            "plant_names", [f"plant_{i}" for i in range(self.params["n"])]
        )

        self.results: Dict[str, DistributedEnergyOptimizerResults] = {}
        self._quadratic_program: Optional[QuadraticProgram] = None
        self._linear_terms: Optional[Dict[str, float]] = None
        self._quadratic_terms: Optional[Dict[Tuple[str, str], float]] = None
        self._offset: Optional[float] = None

    @property
    def offset(self) -> float:
        """
        Offset term property
        """
        if self._offset is None:
            self._linear_terms, self._quadratic_terms, self._offset = self.gen_coeff()
        return self._offset

    @property
    def linear_terms(self) -> Dict[str, float]:
        """
        Linear terms property
        """
        if self._linear_terms is None:
            self._linear_terms, self._quadratic_terms, self._offset = self.gen_coeff()
        return self._linear_terms

    @property
    def quadratic_terms(self) -> Dict[Tuple[str, str], float]:
        """
        Quadratics terms property
        """
        if self._quadratic_terms is None:
            self._linear_terms, self._quadratic_terms, self._offset = self.gen_coeff()
        return self._quadratic_terms

    @property
    def quadratic_program(self) -> QuadraticProgram:
        """
        Quadratic program property
        """
        if self._quadratic_program is None:
            self._quadratic_program = self.gen_quadratic_program()
        return self._quadratic_program

    def parse_params(
        self, arr: List[int], arr_keys: List[str]
    ) -> Tuple[List[int], Dict[Tuple[int, int], int], List[float]]:
        """
        Parse optimal binary state vectors.

        Args:
            arr (List[int]):
                List of 0/1s that represents the state of the binary optimization vars.
                E.g. [0, 0, 0, 1, 1, 0]

            arr_keys (List[str]):
                List of binary optimization variable names corresponding to the state
                values in the arr input.
                E.g. ["xv0", "xv1", "xz00", "xz01", "xz10", "xz11"]

        Returns:
            vs (List[int]):
                List of 0/1s representing whether a power plant is used or not,
                where 0 is turned on and 1 is turned off. This list has n elements,
                where n is the number of plants.

            zs (Dict[Tuple[int,int], int]):
                key (Tuple[int,int]): (i,j) where i represents plant and j represents power level
                val (int): 0/1 representing whether plant i is outputting power level j

            ps (List[float]):
                List of power levels outputted by each plant. This list has n elements,
                where n is the number of plants.
        """
        num_qubits = len(arr)
        n = self.params["n"]
        N = self.params["N"]
        vs = [0 for _ in range(n)]
        zs: Dict[Tuple[int, int], int] = {}

        for i in range(num_qubits):
            val = arr[i]
            key = arr_keys[i]

            # getting v values
            if key[0:2] == "xv":
                v_indx = int(key[2:])
                vs[v_indx] = val

            if key[0:2] == "xz":
                z_indx_str = key[2:]
                i, j = [int(x) for x in z_indx_str.split(",")]
                zs[(i, j)] = val

        ps = [0.0 for _ in range(n)]

        for i in range(n):
            p_min_val = self.params["P_min"][i]
            p_max_val = self.params["P_max"][i]
            h_val = (p_max_val - p_min_val) / N

            if vs[i] == 1:
                continue

            curr_max_indx = 0
            for k in range(N + 1):
                if zs[(i, k)] == 1:
                    curr_max_indx = k

            ps[i] = p_min_val + h_val * curr_max_indx

        return vs, zs, ps

    def gen_coeff(self) -> Tuple[Dict[str, float], Dict[Tuple[str, str], float], float]:
        """
        Based on the parameters provided and stored in self.params.

        Returns:
            linear_terms (Dict[str, float]): 4.2*("xz0,1")
                key (str): represents variable name. E.g. "xz0,1"
                val (str): coefficient of linear term. E.g. 4.2

            quadratic_terms (Dict[Tuple[str,str], float]): 3.2*("xz1,2")*("xz3,0")
                key (Tuple[str,str]): represents cross term between two binary variables. E.g. ("xz1,2". "xz3,0")
                val (float): coefficient of that cross term. E.g. 3.2

            offset (float):
                constant offset
        """
        # setup
        # ==========================================================================
        # parameters
        A = self.params["A"]
        B = self.params["B"]
        C = self.params["C"]
        N = self.params["N"]
        n = self.params["n"]
        p_min = self.params["P_min"]
        p_max = self.params["P_max"]
        alpha = self.params["alpha"]
        beta = self.params["beta"]
        L = self.params["L"]

        # helpers
        def zindx(i: int, k: int) -> str:
            return "xz%s,%s" % (i, k)

        def vindx(i: int) -> str:
            return "xv%s" % i

        h = []
        for i in range(len(p_min)):
            h.append((p_max[i] - p_min[i]) / N)

        linear_terms: Dict[str, float] = {}
        quadratic_terms: Dict[Tuple[str, str], float] = {}
        offset = 0.0

        # cost function
        # ==========================================================================
        # sum_i A_i (1-v_i) done
        for i in range(n):
            linear_terms[vindx(i)] = -A[i]
            offset += A[i]

        # sum_i B_i p_i done
        for i in range(n):
            for k in range(0, N + 1):
                val = B[i] * (p_min[i] + k * h[i])
                linear_terms[zindx(i, k)] = val

        # sum_i C_i p_i^2 done
        for i in range(n):
            for k in range(0, N + 1):
                for m in range(k, N + 1):
                    if m == k:
                        linear_terms[zindx(i, k)] = (
                            linear_terms.get(zindx(i, k), 0)
                            + C[i] * (p_min[i] + k * h[i]) ** 2
                        )
                        continue
                    label1 = (zindx(i, k), zindx(i, m))
                    quadratic_terms[label1] = quadratic_terms.get(label1, 0) + 2 * C[
                        i
                    ] * (p_min[i] + k * h[i]) * (p_min[i] + m * h[i])

        # alpha sum_i (v_i + sum_k z_ik - 1)^2
        for i in range(n):
            linear_terms[vindx(i)] = linear_terms.get(vindx(i), 0) - alpha
            for k in range(0, N + 1):
                linear_terms[zindx(i, k)] += -2 * alpha
                label2 = (vindx(i), zindx(i, k))
                quadratic_terms[label2] = quadratic_terms.get(label2, 0) + 2 * alpha
                for m in range(k, N + 1):
                    if m == k:
                        linear_terms[zindx(i, k)] += alpha
                        continue

                    label3 = (zindx(i, k), zindx(i, m))
                    quadratic_terms[label3] += 2 * alpha
            offset += alpha

        # sum_i p_i = L done
        for i in range(n):
            for k in range(0, N + 1):
                linear_terms[zindx(i, k)] += -2 * beta * L * (p_min[i] + k * h[i])
                for j in range(i, n):
                    for m in range(k, N + 1):
                        if i == j and m == k:
                            linear_terms[zindx(i, k)] += (
                                beta * (p_min[i] + k * h[i]) ** 2
                            )
                            continue
                        label4 = (zindx(i, k), zindx(j, m))

                        quadratic_terms[label4] = quadratic_terms.get(
                            label4, 0
                        ) + 2 * beta * (p_min[i] + k * h[i]) * (p_min[j] + m * h[j])

        offset += beta * L**2

        return linear_terms, quadratic_terms, offset

    # IBM
    # ==============================================================================
    def gen_quadratic_program(self) -> QuadraticProgram:
        """
        Generates Qiskit QuadraticProgram object based on linear terms, quadratic terms,
        and offset of the problem at hand.

        Returns:
            qubo (QuadraticProgram):
                Qiskit QuadraticProgram object describing QUBO optimization problem.
        """
        qubo = QuadraticProgram(name="energy")
        n = self.params["n"]
        N = self.params["N"]

        qubo.binary_var_dict(n, key_format="v{}")
        for i in range(n):
            qubo.binary_var_dict(
                key_format="z" + str(i) + ",{}", keys=list(range(N + 1))
            )

        qubo.minimize(
            linear=self.linear_terms,
            quadratic=self.quadratic_terms,
            constant=self.offset,
        )
        return qubo

    def _run_gate_based_opt(
        self,
        quantum_instance: Optional[QuantumInstance] = None,
        label: str = "qaoa",
        opt_type: str = "qaoa",
    ) -> DistributedEnergyOptimizerResults:
        """
        Base function for gate based QAOA or VQE optimization methods.

        Args:
            quantum_instance (Optional[QuantumInstance]):
                Qiskit backend on which to run quantum optimization.

            label (str):
                label to use for results

            opt_type (str):
                "qaoa" or "vqe"

        Returns:
            results (DistributedEnergyOptimizerResults):
                results from optimization
        """
        opt_types = {"qaoa": QAOA, "vqe": VQE}
        quantum_algo = opt_types[opt_type]

        if quantum_instance is None:
            backend = Aer.get_backend("qasm_simulator")
            quantum_instance = QuantumInstance(
                backend=backend,
                seed_simulator=algorithm_globals.random_seed,
                seed_transpiler=algorithm_globals.random_seed,
            )
        quadprog = self.quadratic_program

        _eval_count = 0

        def callback(eval_count, parameters, mean, std):
            nonlocal _eval_count
            _eval_count = eval_count

        # Create solver
        solver = quantum_algo(
            quantum_instance=quantum_instance,
            callback=callback,
        )

        # Create optimizer for solver
        optimizer = MinimumEigenOptimizer(solver)

        # Get result from optimizer
        result = optimizer.solve(quadprog)

        self.results[label] = DistributedEnergyOptimizerResults(
            result, {"eval_count": _eval_count}
        )
        return self.results[label]

    def run_qaoa(
        self, quantum_instance: Optional[QuantumInstance] = None, label: str = "qaoa"
    ) -> DistributedEnergyOptimizerResults:
        """
        QAOA Optimization method.

        Args:
            quantum_instance (Optional[QuantumInstance]):
                Qiskit backend on which to run quantum optimization.

            label (str):
                label to use for results

        Returns:
            result (DistributedEnergyOptimizerResults):
                results from optimization
        """
        return self._run_gate_based_opt(
            quantum_instance=quantum_instance,
            label=label,
            opt_type="qaoa",
        )

    def run_vqe(
        self, quantum_instance: Optional[QuantumInstance] = None, label: str = "vqe"
    ) -> DistributedEnergyOptimizerResults:
        """
        VQE Optimization method.

        Args:
            quantum_instance (Optional[QuantumInstance]):
                Qiskit backend on which to run quantum optimization.

            label (str):
                label to use for results

        Returns:
            result (DistributedEnergyOptimizerResults):
                results from optimization
        """
        return self._run_gate_based_opt(
            quantum_instance=quantum_instance,
            label=label,
            opt_type="vqe",
        )

    def run_grover(
        self,
        quantum_instance: Optional[QuantumInstance] = None,
        label: str = "grover",
        num_iterations=100,
    ) -> DistributedEnergyOptimizerResults:
        """
        Grover Optimization method.

        Args:
            quantum_instance (Optional[QuantumInstance]):
                Qiskit backend on which to run quantum optimization.

            label (str):
                label to use for results

            num_iterations (int):
                number of iterations to run with grover

        Returns:
            result (DistributedEnergyOptimizerResults):
                results from optimization
        """
        if quantum_instance is None:
            backend = Aer.get_backend("qasm_simulator")
            quantum_instance = QuantumInstance(
                backend=backend,
                seed_simulator=algorithm_globals.random_seed,
                seed_transpiler=algorithm_globals.random_seed,
            )

        quadprog = self.quadratic_program

        n = self.params["n"]
        N = self.params["N"]
        num_qubits = n + N * n
        optimizer = GroverOptimizer(
            num_qubits, num_iterations=num_iterations, quantum_instance=backend
        )

        # Get result from optimizer
        result = optimizer.solve(quadprog)

        self.results[label] = DistributedEnergyOptimizerResults(result)
        return self.results[label]

    def run_classical(
        self, label: str = "classical"
    ) -> DistributedEnergyOptimizerResults:
        """
        Classical Optimization method.

        Args:
            label (str):
                label to use for results

        Returns:
            result (DistributedEnergyOptimizerResults):
                results from optimization
        """
        solver = NumPyMinimumEigensolver()

        # Create optimizer for solver
        optimizer = MinimumEigenOptimizer(solver)

        # Get result from optimizer
        result = optimizer.solve(self.quadratic_program)

        self.results[label] = DistributedEnergyOptimizerResults(result)
        return self.results[label]

    # D-WAVE
    # ==============================================================================
    def _convert_coeff(self):
        """
        Convert coefficients that use {1,-1} instead of {0,1} for the binary variables.

        Map:
            0 ->  1
            1 -> -1
            x -> y
            x = (1-y)/2

        ax1 -> a(1-x1)/2
            -> offset: a/2
            -> linear: (- a/2) x1

        cx1x2 -> c(1 - x1)(1-x2)/4
              -> offset: c/4
              -> linear: (-c/4) x1
              -> linear: (-c/4) x2
              -> quadratic: (c/4) x1x2
        """
        new_linear_terms = {}
        new_quadratic_terms = {}
        new_offset = self.offset

        # linear terms
        for var_name, coeff in self.linear_terms.items():
            new_offset += coeff / 2.0
            new_linear_terms[var_name] = new_linear_terms.get(var_name, 0) + (
                -coeff / 2.0
            )

        # quadratic terms
        for var_names, coeff in self.quadratic_terms.items():
            new_offset += coeff / 4
            var_name1, var_name2 = var_names
            new_linear_terms[var_name1] = new_linear_terms.get(var_name1, 0) + (
                -coeff / 4
            )
            new_linear_terms[var_name2] = new_linear_terms.get(var_name2, 0) + (
                -coeff / 4
            )
            new_quadratic_terms[var_names] = new_quadratic_terms.get(var_names, 0) + (
                coeff / 4
            )
        return new_linear_terms, new_quadratic_terms, new_offset

    def convert_basis(self, y: int) -> int:
        """
        Convert coefficients that use {1,-1} instead of {0,1} for the binary variables.

        Map:
            1  -> 0
            -1 -> 1
            y  -> x
            x  =  (1-y)/2
        """
        return int((1 - y) / 2)

    def run_annealer_sim(
        self, label: str = "annealer_sim", num_shots: int = 100
    ) -> DistributedEnergyOptimizerResults:
        """
        Annealer Optimization method run on a simulator.

        Args:
            label (str):
                label to use for results

            num_shots (int):
                number of shots to run on the experiment

        Returns:
            result (DistributedEnergyOptimizerResults):
                results from optimization
        """
        vartype = dimod.SPIN

        # run classical simulated annealing
        linear_terms, quadratic_terms, offset = self._convert_coeff()

        model = dimod.BinaryQuadraticModel(
            linear_terms, quadratic_terms, offset=offset, vartype=vartype
        )
        sampler = dimod.SimulatedAnnealingSampler()
        response = sampler.sample(model, num_reads=num_shots)

        # store results
        energies = response.record["energy"]
        min_indx = np.argmin(energies)
        opt_values = response.record["sample"][min_indx]
        opt_values = [self.convert_basis(y) for y in opt_values]
        names = list(response.variables)
        self.results[label] = DistributedEnergyOptimizerResults(
            response,
            {
                "opt_cost": energies[min_indx],
                "opt_state": opt_values,
                "names": names,
                "num_shots": num_shots,
            },
        )
        return self.results[label]

    def run_annealer_qpu(
        self,
        label: str = "annealer_qpu",
        num_shots: int = 100,
        device_name: str = "DW_2000Q_6",
    ) -> DistributedEnergyOptimizerResults:
        """
        Annealer Optimization method run on DWAVE annealers.

        Args:
            label (str):
                label to use for results

            num_shots (int):
                number of shots to run on the experiment

            device_name (str):
                DWAVE device name. E.g. "DW_2000Q_6"

        Returns:
            result (DistributedEnergyOptimizerResults):
                results from optimization
        """

        device = "arn:aws:braket:::device/qpu/d-wave/" + device_name
        vartype = dimod.SPIN

        # define BQM
        linear_terms, quadratic_terms, offset = self._convert_coeff()

        model = dimod.BinaryQuadraticModel(
            linear_terms, quadratic_terms, offset=offset, vartype=vartype
        )

        s3_folder = ("amazon-braket-qbraid-jobs", "5f2001ee89-40iitp-2eac-2ein")

        # run BQM: solve with the D-Wave device
        sampler = BraketDWaveSampler(s3_folder, device_arn=device)
        sampler = EmbeddingComposite(sampler)
        response = sampler.sample(model, num_reads=num_shots)

        # store results
        energies = response.record["energy"]
        min_indx = np.argmin(energies)
        opt_values = response.record["sample"][min_indx]
        opt_values = [self.convert_basis(y) for y in opt_values]
        names = list(response.variables)
        self.results[label] = DistributedEnergyOptimizerResults(
            response,
            {
                "opt_cost": energies[min_indx],
                "opt_state": opt_values,
                "names": names,
                "num_shots": num_shots,
            },
        )
        return self.results[label]

    # Visualizations
    # ==============================================================================
    def print_results(self, label: str = "qaoa") -> None:
        """
        Print results.

        Args:
            label (str):
                label to use when extracting optimization results
        """
        results = self.results[label]
        if label in ["qaoa", "vqe", "grover", "classical"]:
            eval_count = results.extras.get("eval_count", 0)

            print(f"Solution found using the {label} method:\n")
            print(f"Minimum Cost: {results.results.fval} ul")
            print(f"Optimal State: ")
            for source_contribution, source_name in zip(
                results.results.x, results.results.variable_names
            ):
                print(f"{source_name}:\t{source_contribution}")

            print(
                f"\nThe solution was found within {eval_count} evaluations of {label}."
            )
        elif label[:8] == "annealer":
            print(f"Solution found using the {label} method:\n")
            opt_cost = results.extras["opt_cost"]
            print(f"Minimum Cost: {opt_cost} ul")
            print(f"Optimal State: ")
            for source_contribution, source_name in zip(
                results.extras["opt_state"], results.extras["names"]
            ):
                print(f"{source_name}:\t{source_contribution}")
            num_shots = results.extras["num_shots"]
            print(f"\nThe solution was found with {num_shots} shots of {label}.")
        else:
            raise NotImplementedError(f"This method is not implemented yet for {label}")

    def plot_histogram(self, label="qaoa") -> None:
        """
        Output results in bar chart.

        Args:
            label (str):
                label to identify results
        """

        if label in ["qaoa", "vqe", "grover", "classical"] or label[:8] == "annealer":
            plant_names = self.params["plant_names"]
            P_min = self.params["P_min"]
            P_max = self.params["P_max"]
        else:
            raise NotImplementedError(f"This method is not implemented yet for {label}")

        print(f"Plot using the {label} method:\n")

        if label in ["qaoa", "vqe", "grover", "classical"]:
            results = self.results[label].results
            var_values = results.x
            var_names = results.variable_names

        elif label[:8] == "annealer":
            var_values = self.results[label].extras["opt_state"]
            var_names = self.results[label].extras["names"]

        _, _, P = self.parse_params(var_values, var_names)
        fig = plt.figure(figsize=(8, 6), dpi=200)
        _ = fig.add_axes([0, 0, 1, 1])
        sns.barplot(
            x=plant_names,
            y=P_max,
            errcolor=".2",
            edgecolor=".2",
            facecolor=(1, 1, 1, 0),
        )
        sns.barplot(x=plant_names, y=P_min, color="gainsboro", edgecolor=".2")
        sns.barplot(x=plant_names, y=P, color="palegreen", edgecolor=".2")
        rcParams["figure.figsize"] = 2, 3
        plt.show()
