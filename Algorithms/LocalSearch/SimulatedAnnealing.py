from math import e
from random import choice, random

from Algorithms.LocalSearch.Neighborhood import random_move_neighborhood
from Algorithms.LocalSearch.BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Problems.AbstractProblem import AbstractProblem
from Utils.Constants import ANNEALING_ALPHA,SA_TEMPERATURE


class SimulatedAnnealing(BaseIterativeLocalSearch):
    def __init__(self, problem: AbstractProblem, max_iter: int):
        super().__init__(problem, max_iter)
        self.temperature = SA_TEMPERATURE

    def neighbour_config(self):
        neighbourhood = random_move_neighborhood(self.current_config)
        return choice(neighbourhood)

    def calc_temp(self) -> float:
        return self.temperature * ANNEALING_ALPHA

    def run(self):
        self.current_config = self.init_config()
        self.current_config_cost = self.cost(self.current_config)
        self.best_config = self.current_config
        self.best_config_cost = self.current_config_cost
        for i in range(self.max_iter):
            print(f"Best config cost: {self.best_config_cost} , {self.problem.printable_data(self.best_config)}")
            self.proposed_config = self.neighbour_config()
            self.temperature = self.calc_temp()
            improvement_delta = self.cost(self.proposed_config) - self.cost(self.current_config)
            if improvement_delta <= 0:
                self.current_config = self.proposed_config
                self.current_config_cost = self.cost(self.current_config)
                if self.current_config_cost < self.best_config_cost:
                    self.best_config = self.current_config
                    self.best_config_cost = self.current_config_cost
            elif e ** (-(improvement_delta / self.temperature)) > random():
                self.current_config = self.proposed_config
        return self.best_config, self.cost(self.best_config)

