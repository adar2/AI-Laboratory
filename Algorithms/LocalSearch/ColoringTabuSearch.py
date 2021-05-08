from random import randint

from Algorithms.LocalSearch.Neighborhood import random_vertex_neighborhood as get_neighborhood
from Problems.GraphColoringProblem import GraphColoringProblem
from Algorithms.LocalSearch.TabuList import TabuList
from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.LocalSearch.UtilFunctions import coloring_init_config, coloring_cost
from Utils.Constants import INITIAL_TABU_TENURE


class ColoringTabuSearch(TabuSearch):
    def __init__(self, problem: GraphColoringProblem, max_iter: int):
        super().__init__(problem, max_iter)
        self.current_coloring = None
        self.states_explored = 0

    # get neighbours
    def neighbour_config(self) -> list:
        neighborhood = get_neighborhood(self.problem.get_search_space(), self.current_config, self.current_coloring)
        self.states_explored += len(neighborhood)
        min_neighbor = None
        min_neighbor_cost = None
        objective_function = self.cost
        for neighbor in neighborhood:
            neighbor_cost = objective_function(neighbor)
            hash_key = self.convert_to_key(neighbor)
            if hash_key not in self.tabu_list and neighbor_cost < objective_function(self.current_config):
                if min_neighbor is None:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
                elif neighbor_cost < min_neighbor_cost:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
        return min_neighbor if min_neighbor is not None else self.current_config

    # greedy algorithm for base config
    def init_config(self):
        return coloring_init_config(self.problem)

    # Objective function (likely to vary between the 3 options)
    def cost(self, config) -> float:
        return coloring_cost(self.problem, config)

    def run(self):
        self.current_config = self.init_config()
        self.current_coloring = max(self.current_config)
        self.current_config_cost = self.cost(self.current_config)
        self.tabu_list = TabuList(len(self.current_config) / 10, INITIAL_TABU_TENURE)
        self.last_config_cost = self.current_config_cost
        for i in range(self.max_iter):
            if self.is_stuck:
                break
            self.print_current_config_state()
            # for stats
            self.iterations_costs.append(self.best_config_cost)
            self.proposed_config = self.current_config if self.current_config_cost == 0 else self.neighbour_config()
            proposed_config_cost = self.cost(self.proposed_config)
            self.last_config_cost = self.current_config_cost
            self.current_config = self.proposed_config
            improvement_delta = self.last_config_cost - proposed_config_cost
            self.current_config_cost = self.cost(self.proposed_config)
            if self.current_config_cost == 0:
                self.update_coloring()
                continue
            hash_key = self.convert_to_key(self.current_config)
            self.tabu_list.add(hash_key)
            self.update_stuck(improvement_delta)  # checks if we're stuck
            self.update_tabu_list(improvement_delta)
            print(f'Tabu List Size: {self.tabu_list.get_size()}')
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
            if vertex_color == self.current_coloring + 1:
                new_config.append(randint(1, self.current_coloring))
            else:
                new_config.append(vertex_color)
        self.current_config = new_config
        self.current_config_cost = self.cost(self.current_config)

    def print_current_config_state(self):
        print(f'Current Coloring: {self.current_coloring}')
        print(f'Current Cost: {self.current_config_cost}')

    @staticmethod
    def convert_to_key(config):
        # convert to tuple of (x,y,demand)
        return tuple(config)

