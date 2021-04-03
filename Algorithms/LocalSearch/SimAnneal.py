from Problems.AbstractProblem import AbstractProblem
from BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Problems.CVRP import CVRP
from Utils.Constants import ANNEALING_ALPHA
from Algorithms.LocalSearch.Neighborhood import random_move_neighborhood
from random import choice, random
from math import e


class SimAnneal(BaseIterativeLocalSearch):
    def __init__(self, problem: AbstractProblem, max_iter: int, temperature: float):
        super().__init__(problem, max_iter)
        self.temperature = temperature

    def neighbour_config(self, current_config):
        neighbourhood = random_move_neighborhood(current_config)
        return choice(neighbourhood)

    def calc_temp(self) -> float:
        return self.temperature * ANNEALING_ALPHA

    def run(self):
        self.current_config = self.init_config()
        self.best_config = self.current_config
        for i in range(self.max_iter):
            print(f"best config : {self.best_config} , cost: {self.cost(self.best_config)}")
            self.proposed_config = self.neighbour_config(self.current_config)
            self.temperature = self.calc_temp()
            improvement_delta = self.cost(self.proposed_config) - self.cost(self.current_config)
            if improvement_delta <= 0:
                self.current_config = self.proposed_config
                if self.cost(self.current_config) < self.cost(self.best_config):
                    self.best_config = self.current_config
            elif e ** ((-improvement_delta) / self.temperature) > random():
                self.current_config = self.proposed_config
        return self.best_config, self.cost(self.best_config)


if __name__ == '__main__':
    max_i = 100
    p = CVRP(10, [((0, 0), 0), ((0, 10), 3), ((-10, 10,), 3), ((0, -10), 3), ((10, -10), 3)])
    s = SimAnneal(p, max_i, 1000)
    s.run()
