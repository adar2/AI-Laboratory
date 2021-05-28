from Algorithms.DiscreteOptimizationSearch.SearchNode import SearchNode
from Problems.AbstarctSearchProblem import AbstractSearchProblem
from Problems.MultiKnapsack import MultiKnapsack
from Utils.MultiKnapSackParsing import multiknapsack_problem_file_parsing
from time import time


class LeastDiscrepancySearch:

    def __init__(self, problem: AbstractSearchProblem) -> None:
        super().__init__()
        self.upper_bound = None
        self.discrepancy = 0
        self.problem = problem
        self.root = self.problem.get_initial_config()
        self.max_discrepancy = len(problem.get_initial_config())
        self.best_solution = None

    def create_node(self, config):
        capacity = self.problem.calc_remaining_capacity(config)[0]
        if capacity < 0:
            return None
        estimation = self.problem.calc_upper_bound(config)
        value = self.problem.calc_value(config)
        return SearchNode(config, capacity, value, estimation)

    def run(self):
        print('Executing ...')
        start_time = time()
        discrepancy_wave = 0
        root_node = self.create_node(self.root)
        while discrepancy_wave < self.max_discrepancy:
            print(f'Current discrepancy {discrepancy_wave}')
            self.upper_bound = None
            solution = self.least_discrepancy_search(root_node, discrepancy_wave)
            if solution is not None:
                if self.best_solution is None or solution.value > self.best_solution.value:
                    self.best_solution = solution
                    # break
            discrepancy_wave += 1
        print(f'Best solution {self.best_solution.config} , score : {self.best_solution.value}')
        print(f'Run time: {time() - start_time}')
        return self.best_solution.config

    def least_discrepancy_search(self, current_node, discrepancy):
        if self.upper_bound and current_node.upper_bound < self.upper_bound:  # prune this node and sub tree
            return None
        candidates = [self.create_node(config) for config in self.problem.expand(current_node.config)]
        if len(candidates) == 0:
            # print(f'Current node config: {current_node.config} , {current_node.value}')
            if not self.upper_bound or current_node.value > self.upper_bound:
                self.upper_bound = current_node.value
            return current_node
        left_child_node = candidates[0]
        right_child_node = candidates[1]
        if discrepancy == 0:
            return self.least_discrepancy_search(left_child_node, discrepancy) if left_child_node else None
        else:
            right_result = self.least_discrepancy_search(right_child_node,
                                                         discrepancy - 1) if right_child_node else None
            left_result = self.least_discrepancy_search(left_child_node, discrepancy) if left_child_node else None
            if right_result is None and left_result is None:
                return None
            elif right_result is None:
                return left_result
            elif left_result is None:
                return right_result
            return right_result if right_result.value > left_result.value else left_result


if __name__ == '__main__':
    profits_dict, capacities, weights = multiknapsack_problem_file_parsing('SENTO2.DAT')
    problem = MultiKnapsack(capacities, weights, profits_dict)
    algo = LeastDiscrepancySearch(problem)
    algo.run()
