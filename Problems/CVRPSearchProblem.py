import copy

from Algorithms.LocalSearch.UtilFunctions import CVRP_init_config
from Problems.AbstarctSearchProblem import AbstractSearchProblem
from Problems.CVRP import CVRP
from Utils.Constants import DEMAND


class CVRPSearchProblem(AbstractSearchProblem):
    def __init__(self, cvrp_problem: CVRP):
        super().__init__()
        self.cvrp_problem = cvrp_problem
        self.locations = self.cvrp_problem.locations
        self.capacity = self.cvrp_problem.capacity
        initial_config = CVRP_init_config(cvrp_problem)
        self.remaining_cities = [self.locations.index(location) for location in initial_config[1:]]

    def get_initial_config(self):
        return [None] * len(self.remaining_cities)

    def get_sorted_configs(self):
        pass

    def calc_upper_bound(self, config):
        upper_bound = 0
        for i in range(len(config)):
            if config[i] is None or config[i] == 0:
                upper_bound += 1
        return upper_bound

    def calc_remaining_capacity(self, config):
        capacity = self.capacity
        for i in range(len(config)):
            if config[i] == 1:
                capacity -= self.locations[self.remaining_cities[i]][DEMAND]
        return capacity, 0

    def calc_value(self, config):
        value = 0
        for i in range(len(config)):
            if config[i] == 1:
                value += 1
        return value

    def update_remaining_locations(self, config):
        current_truck = []
        remaining_cities = copy.copy(self.remaining_cities)
        index = 0
        while index < len(config):
            if config[index] == 1:
                current_truck.append(self.remaining_cities[index])
                remaining_cities.remove(self.remaining_cities[index])
            index += 1
        self.remaining_cities = remaining_cities
        return current_truck

    def expand(self, config) -> list:
        children = []
        for i in range(len(config)):
            if config[i] is None:
                first = copy.copy(config)
                second = copy.copy(config)
                first[i] = 0
                second[i] = 1
                children.append(second)
                children.append(first)
                break
        return children
