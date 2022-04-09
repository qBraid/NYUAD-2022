class VRPSolution:
    def __init__(self, problem, sample, vehicle_limits, solution = None):
        self.problem = problem
        
        if solution != None:
            self.solution = solution
        else:
            result = list()
            vehicle_result = list()
            step = 0
            vehicle = 0

            # Decoding solution from qubo sample
            for (s, dest) in sample:
                if sample[(s, dest)] == 1:
                    if dest != 0:
                        vehicle_result.append(dest)
                    step += 1
                    if vehicle_limits[vehicle] == step:
                        result.append(vehicle_result)
                        step = 0
                        vehicle += 1
                        vehicle_result = list()
                        if len(vehicle_limits) <= vehicle:
                            break

            # Adding first and last magazine.
            for l in result:
                if len(l) != 0:
                    if problem.first_source:
                        l.insert(0, problem.in_nearest_sources[l[0]])
                    if problem.last_source:
                        l.append(problem.out_nearest_sources[l[len(l) - 1]])

            self.solution = result

    # Checks capacity and visiting.
    def check(self):
        capacities = self.problem.capacities
        weights = self.problem.weights
        solution = self.solution
        vehicle_num = 0

        for vehicle_dests in solution:
            cap = capacities[vehicle_num]
            for dest in vehicle_dests:
                cap -= weights[dest]
            vehicle_num += 1
            if cap < 0: 
                return False

        dests = self.problem.dests
        answer_dests = [dest for vehicle_dests in solution for dest in vehicle_dests[1:-1]]
        if len(dests) != len(answer_dests):
            return False

        lists_cmp = set(dests) & set(answer_dests)
        if lists_cmp == len(dests):
            return False

        return True

    def total_cost(self):
        costs = self.problem.costs
        source = self.problem.source
        solution = self.solution
        cost = 0

        for vehicle_dests in solution:
            if vehicle_dests == []:
                continue
            prev = vehicle_dests[0]
            for dest in vehicle_dests[1:]:
                cost += costs[prev][dest]
                prev = dest
            cost += costs[prev][source]

        return cost

    def all_time_costs(self):
        time_costs = self.problem.time_costs
        source = self.problem.source
        solution = self.solution
        result = list()

        for vehicle_dests in solution:
            if vehicle_dests == []:
                result.append(0)
                continue
            prev = vehicle_dests[0]
            cost = 0
            for dest in vehicle_dests[1:]:
                cost += time_costs[prev][dest]
                prev = dest
            result.append(cost)

        return result

    def all_weights(self):
        weights = self.problem.weights
        result = list()

        for vehicle_dests in self.solution:
            weight = 0
            for dest in vehicle_dests:
                weight += weights[dest]
            result.append(weight)

        return result

    def description(self):
        costs = self.problem.costs
        time_costs = self.problem.time_costs
        solution = self.solution

        vehicle_num = 0
        for vehicle_dests in solution:
            time = 0
            cost = 0

            print('Vehicle number ', vehicle_num, ' : ')

            if len(vehicle_dests) == 0:
                print('    Vehicle is not used.')
                continue

            print('    Startpoint : ', vehicle_dests[0])

            dests_num = 1
            prev = vehicle_dests[0]
            for dest in vehicle_dests[1:len(vehicle_dests) - 1]:
                cost += costs[prev][dest]
                time += time_costs[prev][dest]
                print('    Destination number ', dests_num, ' : ', dest, ', reached at time ', time, '.')
                dests_num += 1
                prev = dest

            endpoint = vehicle_dests[len(vehicle_dests) - 1]
            cost += costs[prev][endpoint]
            time += time_costs[prev][endpoint]
            print('    Endpoint : ', endpoint, ', reached at time ', time, '.')

            print('')
            print('    Total cost of vehicle : ', cost)

            vehicle_num += 1

