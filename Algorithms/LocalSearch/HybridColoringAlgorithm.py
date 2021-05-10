from Algorithms.LocalSearch.BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Algorithms.LocalSearch.Neighborhood import random_vertex_neighborhood as get_neighborhood
from Algorithms.LocalSearch.UtilFunctions import coloring_init_config
from Problems.GraphColoringProblem import GraphColoringProblem
from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing
from random import randint
from time import process_time

from Utils.Constants import STUCK_PCT


class HybridColoringAlgorithm(BaseIterativeLocalSearch):

    def __init__(self, problem, max_iter: int):
        super().__init__(problem, max_iter)
        self.graph = self.problem.get_search_space()
        self.current_coloring = None
        self.states_explored = 0
        self.color_classes_dict = {}
        self.bad_edges_dict = {}

    def init_config(self):
        return coloring_init_config(self.problem)

    def neighbour_config(self) -> list:
        neighborhood = get_neighborhood(self.problem.get_search_space(), self.current_config, self.current_coloring)
        self.states_explored += len(neighborhood)
        min_neighbor = None
        min_neighbor_cost = None
        objective_function = self.cost
        for neighbor in neighborhood:
            neighbor_cost = objective_function(neighbor)
            if neighbor_cost < objective_function(self.current_config):
                if min_neighbor is None:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
                elif neighbor_cost < min_neighbor_cost:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
        return min_neighbor if min_neighbor is not None else self.current_config

    def cost(self, config) -> float:
        unique_colors = set(config)
        bad_edges = []
        bad_edges_dict = {key: 0 for key in unique_colors}
        colors_dict = {key: 0 for key in unique_colors}
        for vertex in range(len(config)):
            for constraint_vertex in self.graph[vertex + 1]:
                # avoid adding the bad edge from both sides
                if config[vertex] == config[constraint_vertex - 1] and (constraint_vertex - 1, vertex) not in bad_edges:
                    bad_edges.append((vertex, constraint_vertex - 1))
                    bad_edges_dict[config[vertex]] += 1
        for vertex in config:
            colors_dict[vertex] += 1
        sum1 = 0
        sum2 = 0
        for color in colors_dict:
            sum1 += 2 * bad_edges_dict[color] * colors_dict[color]
            sum2 += colors_dict[color] ** 2
        return sum1 - sum2

    def is_complete(self, config):
        if len(config) != self.problem.vertices:
            return False
        # check that indeed no constraints are violated
        for vertex_1 in self.graph:
            for vertex_2 in self.graph[vertex_1]:
                if config[vertex_1 - 1] == config[vertex_2 - 1]:
                    return False
        return True

    def run(self):
        self.current_config = self.init_config()
        self.current_coloring = max(self.current_config)
        self.current_config_cost = self.cost(self.current_config)
        start_time = process_time()
        print("Executing...")
        for i in range(self.max_iter):
            if self.is_stuck:
                break
            # print(f'Current config objective function value: {self.current_config_cost}')
            neighbor = self.neighbour_config()
            neighbor_cost = self.cost(neighbor)
            improvement_delta = self.current_config_cost - neighbor_cost
            self.update_stuck(improvement_delta)
            if neighbor_cost < self.current_config_cost:
                self.current_config = neighbor
                self.current_config_cost = neighbor_cost
            if self.is_complete(self.current_config):
                print(f"found legal coloring with {self.current_coloring} colors")
                self.reduce_current_config_coloring()
        self.elapsed_time = round(process_time() - start_time, 2)
        print("---------------------")
        print(f"Chromatic number found: {self.current_coloring + 1}")
        print(f'Number of states explored: {self.states_explored}')
        print(f"Time elapsed: {self.elapsed_time}")
        return self.current_coloring + 1

    def reduce_current_config_coloring(self):
        self.current_coloring -= 1
        self.iterations_stuck = 0
        new_config = []
        for vertex_color in self.current_config:
            if vertex_color == self.current_coloring + 1:
                new_config.append(randint(1, self.current_coloring))
            else:
                new_config.append(vertex_color)
        self.current_config = new_config
        self.current_config_cost = self.cost(self.current_config)

    def update_stuck(self, improvement_delta):
        if improvement_delta == 0:
            self.iterations_stuck += 1
        else:
            self.iterations_stuck = 0
        if self.iterations_stuck >= STUCK_PCT * self.max_iter:
            self.is_stuck = True
