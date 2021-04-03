from AbstractProblem import AbstractProblem
from BaseIterativeLocalSearch import BaseIterativeLocalSearch
from random import shuffle
from CVRP import CVRP


class SimAnneal(BaseIterativeLocalSearch):
    def __init__(self, problem: AbstractProblem, max_iter: int, temperature: float):
        super().__init__(problem, max_iter)
        self.temperature = temperature

    def neighbour_config(self) -> list:
        pass

    def calc_temp(self, iteration) -> float:
        pass

    def run(self):
        self.current_config = self.init_config()
        self.best_config = self.current_config
        for i in range(self.max_iter):
            self.proposed_config = self.neighbour_config()
            self.temperature = self.calc_temp(i)
            if self.cost(self.proposed_config) < self.cost(self.current_config):
                self.current_config = self.proposed_config
                if self.cost(self.current_config) < self.cost(self.best_config):
                    self.best_config = self.current_config


if __name__ == '__main__':
    max_iter = 100
    problem = CVRP(10, [((0, 0), 0), ((0, 10), 3), ((-10, 10,), 3), ((0, -10), 3), ((10, -10), 3)])
    s = SimAnneal(problem, max_iter, 0)
    s.run()
