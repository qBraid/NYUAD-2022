from qubo_helper import Qubo

# Attributes : costs dictionary, source, list of destinations
class TSPProblem:
    def __init__(self, costs, source, dests):
        self.costs = costs
        self.source = source
        self.dests = dests

    def get_qubo(self, only_one_const, order_const):
        tsp_qubo = Qubo()
        steps_num = len(self.dests)
        source = self.source

        # Only one vertex for one step.
        for step in range(steps_num):
            tsp_qubo.add_only_one_constraint([(step, i) for i in self.dests], only_one_const)

        # Only one step for one vertex
        for dest in self.dests:
            tsp_qubo.add_only_one_constraint([(step, dest) for step in range(steps_num)], only_one_const)

        # Constraints for first and last destination.
        for dest in self.dests:
            in_index = ((0, dest), (0, dest))
            out_index = (steps_num - 1, dest), (steps_num - 1, dest)
            in_cost = self.costs[source][dest]
            out_cost = self.costs[dest][source]
            tsp_qubo.add(in_index, in_cost * order_const)
            tsp_qubo.add(out_index, out_cost * order_const)

        # Constraints for next steps.
        for step in range(steps_num - 1):
            for i in self.dests:
                for j in self.dests:
                    cost = self.costs[i][j]
                    index = ((step, i), (step + 1, j))
                    tsp_qubo.add(index, cost * order_const)

        return tsp_qubo

    def decode_sample(self, sample):
        result = list()
        for (step, dest) in sample:
            if sample[(step, dest)] == 1:
                result.append(dest)
        return result

    def answer_cost(self, answer):
        total_cost = 0;
        prev = self.answer
        for dest in answer:
            total_cost += self.costs[prev][dest]
        total_cost += self.costs[prev][self.source]
        return total_cost
