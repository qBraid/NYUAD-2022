from vrp_solution import VRPSolution

class VRPTWSolution(VRPSolution):

    TIME_WINDOW_RADIUS = 60
    TIME_BLOCK = 30
    TIME_WINDOWS_DIFF = 30

    def _check_time(self, dest, time):
        time_window = self.problem.time_windows[dest]
        max_time = time_window + self.TIME_WINDOW_RADIUS
        return time <= max_time

    # Small function for waiting simulating.
    def _minimum_time(self, dest, time):
        time_window = self.problem.time_windows[dest]
        min_time = time_window - self.TIME_WINDOW_RADIUS
        return max(time, min_time)

    # Checks capacity, visiting and time.
    def check(self):
        capacities = self.problem.capacities
        weights = self.problem.weights
        time_costs = self.problem.time_costs
        time_windows = self.problem.time_windows
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

        # Time windows checking.
        for vehicle_dests in solution:
            time = 0
            prev = 0
            for dest in vehicle_dests[1:-1]:
                if prev != 0:
                    time += time_costs[prev][dest]
                if not self._check_time(dest, time):
                    return False
                else:
                    time = self._minimum_time(dest, time)
                prev = dest

        return True
