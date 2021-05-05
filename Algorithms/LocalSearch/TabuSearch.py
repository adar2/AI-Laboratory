from Algorithms.LocalSearch.BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Problems.AbstractProblem import AbstractProblem
from Algorithms.LocalSearch.TabuList import TabuList
from Utils.Constants import INITIAL_TABU_TENURE, COORDINATES, CLOCK_RATE, STUCK_PCT
from time import process_time
from abc import abstractmethod


class TabuSearch(BaseIterativeLocalSearch):
    def __init__(self, problem: AbstractProblem, max_iter: int):
        super().__init__(problem, max_iter)
        self.tabu_list = None

    @abstractmethod
    def convert_to_key(self, config):
        raise NotImplementedError

    def run(self):
        self.current_config = self.init_config()
        self.current_config_cost = self.cost(self.current_config)
        self.tabu_list = TabuList(len(self.current_config) / 10, INITIAL_TABU_TENURE)
        self.best_config = self.current_config
        self.best_config_cost = self.cost(self.best_config)
        self.last_config_cost = self.best_config_cost
        start_time = process_time()
        for i in range(self.max_iter):
            if self.is_stuck:
                break
            print(f"Best Config: {self.problem.printable_data(self.best_config)}")
            print(f"Best Config Cost: {self.best_config_cost}")
            print("-----------------")
            self.iterations_costs.append(self.best_config_cost)
            self.proposed_config = self.neighbour_config()
            proposed_config_cost = self.cost(self.proposed_config)
            self.last_config_cost = self.current_config_cost
            self.current_config = self.proposed_config
            improvement_delta = self.last_config_cost - proposed_config_cost
            self.current_config_cost = self.cost(self.proposed_config)
            if self.current_config_cost < self.best_config_cost:
                self.best_config = self.current_config
                self.best_config_cost = self.current_config_cost
            current_config_hash_key = self.convert_to_key(self.current_config)
            self.tabu_list.add(current_config_hash_key)
            self.update_stuck(improvement_delta)  # checks if we're stuck
            if improvement_delta > 0:
                self.tabu_list.capacity -= 1
            elif abs(improvement_delta) > 0.05 * self.last_config_cost:
                self.tabu_list.capacity += 1
                self.tabu_list.tenure += 1
            self.tabu_list.update()
        print(f'Final Cost: {self.best_config_cost}')
        self.elapsed_time = round(process_time() - start_time, 2)
        self.clock_ticks = self.elapsed_time * CLOCK_RATE
        return self.best_config_cost

    def update_stuck(self, improvement_delta):
        if improvement_delta == 0:
            self.iterations_stuck += 1
        else:
            self.iterations_stuck = 0
        if self.iterations_stuck >= STUCK_PCT * self.max_iter:
            self.is_stuck = True

    @abstractmethod
    def neighbour_config(self) -> list:
        raise NotImplementedError
