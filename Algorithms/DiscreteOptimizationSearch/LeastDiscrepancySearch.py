from Algorithms.DiscreteOptimizationSearch.SearchNode import SearchNode
from Problems.AbstarctSearchProblem import AbstractSearchProblem


class LeastDiscrepancySearch:

    def __init__(self, problem: AbstractSearchProblem) -> None:
        super().__init__()
        self.problem = problem
        self.initial_items_list = problem.get_sorted_configs()

    def create_node(self, config, discrepancy=0, item_to_expand=0):
        child_discrepancy = 0 if discrepancy == 0 else discrepancy + 1
        child_config = config
        child_upper_bound = self.problem.calc_upper_bound(config)
        child_capacity = self.problem.calc_remaining_capacity(config)
        child_value = self.problem.calc_value(config)
        child_item_to_expand = item_to_expand
        return SearchNode(child_config,child_upper_bound,child_capacity,child_value,child_discrepancy,child_item_to_expand)

    def run(self):
        discrepancy_wave = 0
        solution = None
        # TODO: find upper bound of discrepancy?
        while True:
            solution = self.least_discrepancy_search(discrepancy_wave)
            if solution is not None:
                break
            discrepancy_wave += 1
        return solution

    def least_discrepancy_search(self, discrepancy_wave):
        raise NotImplementedError


