"""
DistributedEnergyOptimizer
"""

from typing import Dict, Any, Tuple
from qiskit_optimization import QuadraticProgram
from qiskit import Aer
from qiskit.algorithms import QAOA, VQE, NumPyMinimumEigensolver
from qiskit_optimization.algorithms import MinimumEigenOptimizer, GroverOptimizer
from qiskit.utils import QuantumInstance, algorithm_globals
import dimod


# def gen_transportation_losses():
#     return "Transportation Loss": [(A1,B1,C1),(A2,B2,C2),(A3,B3,C3)],

# def gen_model_parameters(cost_types: Dict[str, List[Tuple[float,float,float]]], weights: List[float]):
#     """
#     TODO: docstrings


#     cost_types = {
#         "CO2": [(A1,B1,C1),(A2,B2,C2),(A3,B3,C3)],
#         "Efficiency": [(A1,B1,C1),(A2,B2,C2),(A3,B3,C3)],
#         "Transportation Loss": [(A1,B1,C1),(A2,B2,C2),(A3,B3,C3)],
#     }
#     Args:
#         cost_type:
#             key (str): e.g. CO2 emissions
#             val (list[tuple(float,float,float)]): [(A, B, C),...]
#     """

#     n = len(list(cost_types.values())[0])

#     A = [0 for _ in range(n)]
#     B = [0 for _ in range(n)]
#     C = [0 for _ in range(n)]

#     for cost_type, costs in cost_types.items():
#         for plant_indx in range(n):
#             A[plant_indx] +=  weight[costs[plant_indx][0]


class DistributedEnergyOptimizer:
    """
    Optimizing unit commitment from a distributed energy network.
    """

    REQUIRED_PARAMS = ["A", "B", "C", "P_min", "P_max", "L", "N"]

    def __init__(self, params) -> None:

        for label in self.REQUIRED_PARAMS:  # make sure we have all the required params
            if label not in params:
                raise ValueError(f"Please provide {label} in params.")

        self.params = params.copy()
        self.params["alpha"] = params.get("alpha", 5e5)  # TODO: check if ok default
        self.params["beta"] = params.get("beta", 8)  # TODO: check if ok default

        self.results: Dict[str, Any] = {}
        self._quadratic_program = None
        self._linear_terms = None
        self._quadratic_terms = None
        self._offset = None

    @property
    def offset(self):
        """
        Offset
        """
        if self._offset is None:
            self._linear_terms, self._quadratic_terms, self._offset = self.gen_coeff()
        return self._offset

    @property
    def linear_terms(self):
        """
        Linear Terms
        """
        if self._linear_terms is None:
            self._linear_terms, self._quadratic_terms, self._offset = self.gen_coeff()
        return self._linear_terms

    @property
    def quadratic_terms(self):
        """
        Quadratics Terms
        """
        if self._quadratic_terms is None:
            self._linear_terms, self._quadratic_terms, self._offset = self.gen_coeff()
        return self._quadratic_terms

    @property
    def quadratic_program(self):
        """
        Quadratic Program
        """
        if self._quadratic_terms is None:
            self._quadratic_program = self.gen_quadratic_program()
        return self._quadratic_program

    def gen_coeff(self):
        # setup
        # ==========================================================================
        # parameters
        A = self.params["A"]
        B = self.params["B"]
        C = self.params["C"]
        N = self.params["N"]
        n = len(A)
        p_min = self.params["P_min"]
        p_max = self.params["P_max"]
        alpha = self.params["alpha"]
        beta = self.params["beta"]
        L = self.params["L"]

        # helpers
        def zindx(i: int, k: int) -> str:
            return "xz%s%s" % (i, k)

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
        # A_i (1-v_i)
        for i in range(n):
            linear_terms[vindx(i)] = -A[i]
        offset += alpha

        # B_i p_i
        for i in range(n):
            for k in range(0, N + 1):
                linear_terms[zindx(i, k)] = B[i] * (p_min[i] + k * h[i])

        # C_i p_i^2
        for i in range(n):
            for k in range(0, N + 1):
                for m in range(k, N + 1):
                    if m == k:
                        linear_terms[zindx(i, k)] = (
                            linear_terms.get(zindx(i, k), 0)
                            + linear_terms.get(zindx(i, k), 0)
                            + C[i] * (p_min[i] + k * h[i]) ** 2
                        )
                        continue
                    label1 = (zindx(i, k), zindx(i, m))
                    quadratic_terms[label1] = quadratic_terms.get(label1, 0) + 2 * C[
                        i
                    ] * (p_min[i] + k * h[i]) * (p_min[i] + m * h[i])

        # v_i + sum_k z_ik = 1
        for i in range(n):
            linear_terms[vindx(i)] = linear_terms.get(vindx(i), 0) - alpha
            for k in range(0, N + 1):
                linear_terms[zindx(i, k)] += -2 * alpha
                label2 = (vindx(i), zindx(i, k))
                quadratic_terms[label2] = quadratic_terms.get(label2, 0) + 2 * alpha
                for m in range(k, N + 1):
                    if m == k:
                        linear_terms[zindx(i, k)] = 2 * alpha
                        continue

                    label3 = (zindx(i, k), zindx(i, m))
                    quadratic_terms[label3] += 4 * alpha
        offset += alpha

        # sum_i p_i = L
        for i in range(n):
            for k in range(0, N + 1):
                linear_terms[zindx(i, k)] += -2 * beta * L * (p_min[i] + k * h[i])
                for j in range(i, n):
                    for m in range(k, N + 1):
                        if i == j and m == k:
                            linear_terms[zindx(i, k)] = (
                                beta * (p_min[i] + k * h[i]) ** 2
                            )
                            continue
                        label4 = (zindx(i, k), zindx(j, m))
                        quadratic_terms[label4] = quadratic_terms.get(
                            label4, 0
                        ) + 4 * beta * (p_min[i] + k * h[i]) * (p_min[j] + m * h[j])
        offset += beta * L**2

        return linear_terms, quadratic_terms, offset

    # IBM
    # ==============================================================================
    def gen_quadratic_program(self):
        """
        TODO: write docstring
        """
        qubo = QuadraticProgram(name="energy")
        n = len(self.params["A"])
        N = self.params["N"]

        qubo.binary_var_dict(n, key_format="v{}")
        for i in range(n):
            qubo.binary_var_dict(
                key_format="z" + str(i) + "{}", keys=list(range(N + 1))
            )

        qubo.minimize(
            linear=self.linear_terms,
            quadratic=self.quadratic_terms,
            constant=self.offset,
        )
        return qubo

    def _run_gate_based_opt(self, quantum_instance=None, label="qaoa", opt_type="qaoa"):
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

        self.results[label] = {
            "results": result,
            "eval_count": _eval_count,
        }
        return self.results[label]

    def run_qaoa(self, quantum_instance=None, label="qaoa"):
        """
        TODO: qaoa
        """
        return self._run_gate_based_opt(
            quantum_instance=quantum_instance,
            label=label,
            opt_type="qaoa",
        )

    def run_vqe(self, quantum_instance=None, label="vqe"):
        """
        TODO: qaoa
        """
        return self._run_gate_based_opt(
            quantum_instance=quantum_instance,
            label=label,
            opt_type="vqe",
        )

    def run_grover(self, quantum_instance=None, label="grover"):
        """
        Grover
        """
        if quantum_instance is None:
            backend = Aer.get_backend("qasm_simulator")
            quantum_instance = QuantumInstance(
                backend=backend,
                seed_simulator=algorithm_globals.random_seed,
                seed_transpiler=algorithm_globals.random_seed,
            )

        quadprog = self.quadratic_program

        n = len(self.params["A"])
        N = self.params["N"]
        num_qubits = n + N * n
        optimizer = GroverOptimizer(
            num_qubits, num_iterations=100, quantum_instance=backend
        )

        # Get result from optimizer
        result = optimizer.solve(quadprog)

        self.results[label] = {
            "results": result,
        }
        return self.results[label]

    def run_classical(self, label="classical"):
        """
        TODO: docstring
        """
        solver = NumPyMinimumEigensolver()

        # Create optimizer for solver
        optimizer = MinimumEigenOptimizer(solver)

        # Get result from optimizer
        result = optimizer.solve(self.quadratic_program)

        self.results[label] = {
            "results": result,
        }
        return self.results[label]

    # D-WAVE
    # ==============================================================================
    def run_qubo(self, label="qubo"):
        """
        TODO: qubo
        """
        num_shots = 100
        offset = 0
        vartype = dimod.SPIN

        # run classical simulated annealing
        model = dimod.BinaryQuadraticModel(
            self.linear_terms, self.quadratic_terms, offset, vartype
        )
        sampler = dimod.SimulatedAnnealingSampler()
        response = sampler.sample(model, num_reads=num_shots)

        # print results
        self.results[label] = {
            "results": response,
        }
        return self.results[label]

    # Visualizations
    # ==============================================================================
    def print_results(self, label="qaoa"):
        """
        Print results
        """
        qaoa_result = self.results[label]["results"]
        qaoa_eval_count = self.results[label].get("eval_count", 0)

        print(f"Solution found using the {label} method:\n")
        print(f"Minimum Cost: {qaoa_result.fval} ul")
        print(f"Optimal State: ")
        for source_contribution, source_name in zip(
            qaoa_result.x, qaoa_result.variable_names
        ):
            print(f"{source_name}:\t{source_contribution}")

        print(
            f"\nThe solution was found within {qaoa_eval_count} evaluations of {label}."
        )
