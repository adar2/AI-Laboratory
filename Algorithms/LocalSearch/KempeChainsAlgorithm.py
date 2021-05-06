from BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Problems.GraphColoringProblem import GraphColoringProblem
from UtilFunctions import coloring_init_config
import copy
from random import randint, choice
from math import sqrt

from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing


class KempeChainAlgorithm(BaseIterativeLocalSearch):

    def __init__(self, problem: GraphColoringProblem, max_iter: int):
        super().__init__(problem, max_iter)
        self.problem = problem
        self.color_classes_dict = {}
        self.graph = self.problem.get_search_space()
        self.reachable_dict = {}

    def init_config(self):
        return coloring_init_config(self.problem)

    def update_color_classes(self):
        unique_colors = set(self.current_config)
        self.color_classes_dict = {key: [] for key in unique_colors}
        for vertex in range(len(self.current_config)):
            color = self.current_config[vertex]
            self.color_classes_dict[color].append(vertex + 1)

    def neighbour_config(self) -> list:
        neighborhood = []
        graph = self.graph
        config = self.current_config
        number_of_vertices = randint(2, int(sqrt(len(config))))
        vertex_list = []
        for i in range(number_of_vertices):
            random_vertex = randint(1, len(graph))
            while random_vertex in vertex_list:
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

    def kill_color(self):
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

    def is_complete(self,config):
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
        self.current_config_cost = self.cost(self.current_config)
        for i in range(self.max_iter):
            self.update_color_classes()
            self.kill_color()
            print(f'Best config yet {self.current_config_cost}')
            print(f'Current color classes {self.number_of_color_classes()}')
            neighborhood = self.neighbour_config()
            for config in neighborhood:
                if self.cost(config) > self.current_config_cost:
                    self.current_config = config
                    self.current_config_cost = self.cost(config)
        for color in self.color_classes_dict:
            print(f"Color class {color} , size : {self.color_classes_dict[color]}")
        print(f'The Config has passed the test? : {self.is_complete(self.current_config)}')

    def kempe_chain_generator(self, random_vertex, config: list):
        new_config = copy.copy(config)
        random_vertex_color = config[random_vertex - 1]
        adjacent_vertices = [vertex for vertex in self.graph[random_vertex] if
                             config[vertex - 1] != random_vertex_color]
        adjacent_vertex = choice(adjacent_vertices)
        adjacent_vertex_color = config[adjacent_vertex - 1]
        if random_vertex not in self.reachable_dict:
            random_vertex_reachable = set()
            self.__get_reachable_vertices(random_vertex, random_vertex_reachable)
            self.reachable_dict[random_vertex] = random_vertex_reachable
        else:
            random_vertex_reachable = self.reachable_dict[random_vertex]
        if adjacent_vertex not in self.reachable_dict:
            adjacent_vertex_reachable = set()
            self.__get_reachable_vertices(adjacent_vertex, adjacent_vertex_reachable)
            self.reachable_dict[adjacent_vertex] = adjacent_vertex_reachable
        else:
            adjacent_vertex_reachable = self.reachable_dict[adjacent_vertex]
        kempe_chain = list(random_vertex_reachable | adjacent_vertex_reachable)
        kempe_chain = [vertex for vertex in kempe_chain if
                       config[vertex - 1] == random_vertex_color or config[vertex - 1] == adjacent_vertex_color]
        for vertex in kempe_chain:
            if config[vertex - 1] == random_vertex_color:
                new_config[vertex - 1] = adjacent_vertex_color
            elif config[vertex - 1] == adjacent_vertex_color:
                new_config[vertex - 1] = random_vertex_color
        self.is_complete(new_config)
        return new_config

    def __get_reachable_vertices(self, vertex: int, reachable_vertices: set) -> set:
        for neighbor_1 in self.graph[vertex]:
            if neighbor_1 in reachable_vertices:
                continue
            reachable_vertices.add(neighbor_1)
            reachable_vertices = reachable_vertices.union(self.__get_reachable_vertices(neighbor_1, reachable_vertices))
        return reachable_vertices


if __name__ == '__main__':
    graph1, vertices, edges = coloring_problem_file_parsing('le450_15a.col')
    problem = GraphColoringProblem(graph1, vertices, edges)
    algo = KempeChainAlgorithm(problem, 1000)
    algo.run()
