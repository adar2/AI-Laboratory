from Algorithms.LocalSearch.UtilFunctions import CVRP_init_config
from Problems.AbstarctSearchProblem import AbstractSearchProblem
from Problems.CVRP import CVRP


class CVRPSearchProblem(AbstractSearchProblem):
    def __init__(self, cvrp_problem: CVRP):
        super().__init__()
        self.cvrp_problem = cvrp_problem

    def get_initial_config(self):
        return CVRP_init_config(self.cvrp_problem)

    def get_sorted_configs(self):
        pass

    def calc_upper_bound(self, config):
        pass

    def calc_remaining_capacity(self, config):
        pass

    def calc_value(self, config):
        pass

    def expand(self, config) -> list:
        pass
