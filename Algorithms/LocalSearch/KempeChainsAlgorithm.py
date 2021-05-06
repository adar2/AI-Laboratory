import copy
from math import sqrt
from random import randint, choice

from Algorithms.LocalSearch.BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Problems.GraphColoringProblem import GraphColoringProblem
from Algorithms.LocalSearch.UtilFunctions import coloring_init_config
from Utils.Constants import STUCK_PCT


class KempeChainsAlgorithm(BaseIterativeLocalSearch):

    def __init__(self, problem: GraphColoringProblem, max_iter: int):
        super().__init__(problem, max_iter)
        self.problem = problem
        self.color_classes_dict = {}
        self.graph = self.problem.get_search_space()

    def init_config(self):
        return coloring_init_config(self.problem)

    def update_color_classes(self):
        unique_colors = set(self.current_config)
        self.color_classes_dict = {key: [] for key in unique_colors}
        for vertex in range(len(self.current_config)):
            color = self.current_config[vertex]
            self.color_classes_dict[color].append(vertex + 1)

    def updated_stuck(self, updated):
        if not updated:
            self.iterations_stuck += 1
        else:
            self.iterations_stuck = 0
        if self.iterations_stuck >= STUCK_PCT * self.max_iter:
            self.is_stuck = True

    def neighbour_config(self) -> list:
        neighborhood = []
        graph = self.graph
        config = self.current_config
        number_of_vertices = randint(2, int(sqrt(len(config))))
        vertex_list = []
        for i in range(number_of_vertices):
            random_vertex = randint(1, len(graph))
            while random_vertex in vertex_list or not self.graph[random_vertex]:
                random_vertex = randint(1, len(graph))
            vertex_list.append(random_vertex)
            new_config = self.kempe_chain_generator(random_vertex, config)
            neighborhood.append(new_config)
        return neighborhood

    def cost(self, config) -> float:
        unique_colors = set(config)
        colors_dict = {key: 0 for key in unique_colors}
        for vertex in config:
            colors_dict[vertex] += 1
        sum = 0
        for color in colors_dict:
            sum += colors_dict[color] ** 2
        return sum

    def number_of_color_classes(self):
        sum = 0
        for color in self.color_classes_dict:
            if len(self.color_classes_dict[color]) > 0:
                sum += 1
        return sum

    def remove_color(self):
        for color in self.color_classes_dict:
            if len(self.color_classes_dict[color]) == 1:
                vertex = self.color_classes_dict[color][0]
                colors_domain = list(range(1, len(self.color_classes_dict) + 1))
                for neighbor in self.graph[vertex]:
                    neighbor_color = self.current_config[neighbor - 1]
                    if neighbor_color in colors_domain:
                        colors_domain.remove(neighbor_color)
                if len(colors_domain) > 1:
                    colors_domain.remove(color)
                    remaining_color = colors_domain[0]
                    self.current_config[vertex - 1] = remaining_color
                    self.color_classes_dict[remaining_color].append(vertex)
                    self.color_classes_dict[color].remove(vertex)

    def run(self):
        self.current_config = self.init_config()
        self.current_config_cost = self.cost(self.current_config)
        for i in range(self.max_iter):
            if self.is_stuck:
                break
            updated = False
            self.update_color_classes()
            self.remove_color()
            print(f'Best config yet {self.current_config_cost}')
            print(f'Current color classes {self.number_of_color_classes()}')
            neighborhood = self.neighbour_config()
            for config in neighborhood:
                if self.cost(config) > self.current_config_cost:
                    updated = True
                    self.current_config = config
                    self.current_config_cost = self.cost(config)
            self.updated_stuck(updated)
        print(f'The chromatic color found for current problem : {len(self.color_classes_dict)}')

    def kempe_chain_generator(self, random_vertex, config: list):
        new_config = copy.copy(config)
        random_vertex_color = config[random_vertex - 1]
        adjacent_vertices = [vertex for vertex in self.graph[random_vertex] if
                             config[vertex - 1] != random_vertex_color]
        adjacent_vertex = choice(adjacent_vertices)
        adjacent_vertex_color = config[adjacent_vertex - 1]
        kempe_chain = [random_vertex, adjacent_vertex]
        random_vertex_reachable = set(kempe_chain)
        self.__get_reachable_vertices(random_vertex, random_vertex_reachable, color_1=random_vertex_color,
                                      color_2=adjacent_vertex_color)
        adjacent_vertex_reachable = set(kempe_chain)
        self.__get_reachable_vertices(adjacent_vertex, adjacent_vertex_reachable, color_1=adjacent_vertex_color,
                                      color_2=random_vertex_color)
        kempe_chain = list(random_vertex_reachable | adjacent_vertex_reachable)
        for vertex in kempe_chain:
            if config[vertex - 1] == random_vertex_color:
                new_config[vertex - 1] = adjacent_vertex_color
            elif config[vertex - 1] == adjacent_vertex_color:
                new_config[vertex - 1] = random_vertex_color
        return new_config

    def __get_reachable_vertices(self, vertex: int, reachable_vertices: set, color_1: int, color_2: int) -> set:
        for neighbor_1 in self.graph[vertex]:
            if neighbor_1 in reachable_vertices:
                continue
            if self.current_config[neighbor_1 - 1] == color_2:
                reachable_vertices.add(neighbor_1)
                self.__get_reachable_vertices(neighbor_1, reachable_vertices, color_2, color_1)
        return reachable_vertices

