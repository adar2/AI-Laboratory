from Problems.AbstractProblem import AbstractProblem
from BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Problems.CVRP import CVRP
from Utils.Constants import ANNEALING_ALPHA
from Algorithms.LocalSearch.Neighborhood import random_move_neighborhood
from random import choice, random
from math import e
from Utils.CVRPFileParsing import parse_cvrp_file
from os import getcwd


class SimAnneal(BaseIterativeLocalSearch):
    def __init__(self, problem: AbstractProblem, max_iter: int, temperature: float):
        super().__init__(problem, max_iter)
        self.temperature = temperature

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
            print(f"best config cost: {self.best_config_cost}")
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


if __name__ == '__main__':
    max_i = 5000
    capacity, locations = parse_cvrp_file(getcwd() + '\E-n22-k4.txt')
    p = CVRP(capacity, locations)
    s = SimAnneal(p, max_i, 2000)
    s.run()
