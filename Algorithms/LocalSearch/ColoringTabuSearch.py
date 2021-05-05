from Problems.AbstractProblem import AbstractProblem
from Problems.GraphColoringProblem import GraphColoringProblem
from TabuSearch import TabuSearch
from TabuList import TabuList
from Utils.Constants import INITIAL_TABU_TENURE
from UtilFunctions import coloring_init_config,coloring_cost
from random import randint


class ColoringTabuSearch(TabuSearch):
    def __init__(self, problem: GraphColoringProblem, max_iter: int):
        super().__init__(problem, max_iter)
        self.current_coloring = None
        self.states_explored = 0

    # get neighbours
    def neighbour_config(self) -> list:
        pass

    # greedy algorithm for base config
    def init_config(self):
        return coloring_init_config(self.problem)

    # Objective function (likely to vary between the 3 options)
    def cost(self, config) -> float:
        return coloring_cost(self.problem,config)

    def run(self):
        self.current_config = self.init_config()
        self.current_coloring = max(self.current_config)
        self.current_config_cost = self.cost(self.current_config)
        self.tabu_list = TabuList(len(self.current_config) / 10, INITIAL_TABU_TENURE)
        self.best_config = self.current_config
        self.best_config_cost = self.cost(self.best_config)
        self.last_config_cost = self.best_config_cost
        for i in range(self.max_iter):
            if self.is_stuck:
                break
            self.print_best_config_state()
            # for stats
            self.iterations_costs.append(self.best_config_cost)
            self.proposed_config = self.current_config if self.current_config_cost == 0 else self.neighbour_config()
            proposed_config_cost = self.cost(self.proposed_config)
            self.last_config_cost = self.current_config_cost
            self.current_config = self.proposed_config
            improvement_delta = self.last_config_cost - proposed_config_cost
            self.current_config_cost = self.cost(self.proposed_config)
            self.update_best_config()
            if self.best_config_cost == 0:
                self.update_coloring()
                continue
            self.tabu_list.add(self.current_config)
            self.update_stuck(improvement_delta)  # checks if we're stuck
            self.update_tabu_list(improvement_delta)
        print('--------------------------------------')
        print(f'Chromatic Coloring Found: {self.current_coloring + 1}')
        print(f'Number of states explored: {self.states_explored}')
        return self.current_coloring + 1

    def update_coloring(self):
        print(f'Found Coloring using {self.current_coloring} colors!')
        self.current_coloring -= 1
        self.iterations_stuck = 0
        self.tabu_list = TabuList(len(self.current_config) / 10, INITIAL_TABU_TENURE)
        self.reduce_current_config_coloring()

    def reduce_current_config_coloring(self):
        new_config = []
        for vertex_color in self.current_config:
            if vertex_color == self.current_coloring+1:
                new_config.append(randint(1,self.current_coloring+1))
            else:
                new_config.append(vertex_color)
        self.current_config = new_config
        self.current_config_cost = self.cost(self.current_config)
