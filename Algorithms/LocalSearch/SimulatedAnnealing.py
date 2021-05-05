from math import e
from random import random
import time
from Algorithms.LocalSearch.Neighborhood import random_move_neighborhood
from Algorithms.LocalSearch.BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Problems.AbstractProblem import AbstractProblem
from Utils.Constants import ANNEALING_ALPHA, SA_TEMPERATURE,CLOCK_RATE, STUCK_PCT
from UtilFunctions import cvrp_path_cost, CVRP_init_config


class SimulatedAnnealing(BaseIterativeLocalSearch):
    def __init__(self, problem: AbstractProblem, max_iter: int):
        super().__init__(problem, max_iter)
        self.temperature = SA_TEMPERATURE
        self.cost = cvrp_path_cost
        self.init_config = CVRP_init_config

    def neighbour_config(self):
        neighbourhood = random_move_neighborhood(self.current_config)
        neighbourhood_costs = [self.cost(self.problem,neighbour) for neighbour in neighbourhood]
        return neighbourhood[neighbourhood_costs.index(min(neighbourhood_costs))]

    def calc_temp(self) -> float:
        return self.temperature * ANNEALING_ALPHA

    def update_stuck(self, improvement_delta):
        if improvement_delta == 0:
            self.iterations_stuck += 1
        else:
            self.iterations_stuck = 0
        if self.iterations_stuck >= STUCK_PCT * self.max_iter:
            self.is_stuck = True

    def run(self):
        start_time = time.time()
        self.current_config = self.init_config(self.problem)
        self.current_config_cost = self.cost(self.problem,self.current_config)
        self.best_config = self.current_config
        self.best_config_cost = self.current_config_cost
        for i in range(self.max_iter):
            if self.is_stuck:
                break
            print(f"Best Config: {self.problem.printable_data(self.best_config)}")
            print(f"Best Config Cost: {self.best_config_cost}")
            print("-----------------")
            self.iterations_costs.append(self.best_config_cost)
            self.proposed_config = self.neighbour_config()
            self.temperature = self.calc_temp()
            improvement_delta = self.cost(self.problem,self.proposed_config) - self.cost(self.problem,self.current_config)
            self.update_stuck(improvement_delta)
            if improvement_delta <= 0:
                self.current_config = self.proposed_config
                self.current_config_cost = self.cost(self.problem,self.current_config)
                if self.current_config_cost < self.best_config_cost:
                    self.best_config = self.current_config
                    self.best_config_cost = self.current_config_cost
            elif random() <= e ** (-(improvement_delta / self.temperature)):
                self.current_config = self.proposed_config
        self.elapsed_time = round(time.time() - start_time, 2)
        self.clock_ticks = self.elapsed_time*CLOCK_RATE
        print(f"Time elapsed {self.elapsed_time}")
        return self.best_config, self.cost(self.problem,self.best_config)
