from Algorithms.LocalSearch.BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Neighborhood import random_vertex_neighborhood as get_neighborhood
from UtilFunctions import coloring_init_config


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
            if  neighbor_cost < objective_function(self.current_config):
                if min_neighbor is None:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
                elif neighbor_cost < min_neighbor_cost:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
        return min_neighbor if min_neighbor is not None else self.current_config

    def cost(self, config) -> float:
        bad_edges = []
        for vertex in range(len(config)):
            for constraint_vertex in self.graph[vertex + 1]:
                # avoid adding the bad edge from both sides
                if config[vertex] == config[constraint_vertex - 1] and (constraint_vertex - 1, vertex) not in bad_edges:
                    bad_edges.append((vertex, constraint_vertex - 1))
        unique_colors = set(config)
        colors_dict = {key: 0 for key in unique_colors}
        for vertex in config:
            colors_dict[vertex] += 1
        sum = 0
        for color in colors_dict:
            sum += colors_dict[color] ** 2
        return sum

    def run(self):
        self.current_config = self.init_config()
        self.current_coloring = max(self.current_config)
        self.current_config_cost = self.cost(self.current_config)
        for i in range(self.max_iter):
        pass

