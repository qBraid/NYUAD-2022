from itertools import product

# Simple class helping creating qubo dict.
class Qubo:
    def __init__(self):
        self.dict = dict()
        #self.satisfied_energy = 0

    def create_field(self, field):
        self.dict[field] = 0

    def create_not_exist_field(self, field):
        if field in self.dict:
            return
        self.create_field(field)

    def add_only_one_constraint(self, variables, const):
        for var in variables:
            self.create_not_exist_field((var, var))
            self.dict[(var, var)] -= 2 * const
        for field in product(variables, variables):
            self.create_not_exist_field(field)
            self.dict[field] += const
        #self.satisfied_energy -= const

    def add_and_gate(self, x, y, z, const):
        self.add((x, y), const)
        self.add((x, z), (-2) * const)
        self.add((y, z), (-2) * const)
        self.add((z, z), 3 * const)

    def add(self, field, value):
        self.create_not_exist_field(field)
        self.dict[field] += value

    def merge_with(self, qubo, const1, const2):
        for field in self.dict:
            self.dict[field] *= const1
        for field in qubo.dict:
            self.create_not_exist_field(field)
            self.dict[field] += qubo.dict[field] * const2
        #self.satisfied_energy += qubo.satisfied_energy

    def get_dict(self):
        return self.dict
