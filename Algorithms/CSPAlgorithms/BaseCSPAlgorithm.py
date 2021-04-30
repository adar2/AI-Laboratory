from abc import ABC, abstractmethod
from Problems.AbstractProblem import AbstractProblem
from random import choice


class BaseCSPAlgorithm(ABC):

    def __init__(self, problem: AbstractProblem) -> None:
        super().__init__()
        self.problem = problem
        self.graph = problem.get_search_space()
        self.constraints_dict = problem.get_search_space()
        # start from two because we must have at least one color
        self.next_color = 2
        self.current_color = 1
        self.color_groups_dict = {1: []}  # 1: [5,4,1] 2: 6,7,8
        self.vertices_color_dict = {}  # 1:2

    def update_vertex(self, vertex: int, color: int):
        if vertex in self.vertices_color_dict.keys():
            self.color_groups_dict[self.vertices_color_dict[vertex]].remove(vertex)
        self.vertices_color_dict[vertex] = color
        if color not in self.color_groups_dict:
            self.color_groups_dict[color] = []
        self.color_groups_dict[color].append(vertex)

    # return true if assignment is complete false otherwise
    def is_complete(self):
        if len(self.vertices_color_dict) != self.problem.vertices:
            return False
        # check that indeed no constraints are violated
        for vertex in self.vertices_color_dict.keys():
            for v2 in self.constraints_dict[vertex]:
                if self.vertices_color_dict[vertex] == self.vertices_color_dict[v2]:
                    return False
        return True

    # return some unassigned variable by some method/ heuristic
    def select_unassigned_variable(self, heuristic=None):
        if heuristic is None:
            # generate list of unassigned keys (vertices)
            unassigned_variable = [key for key in self.graph.keys() if key not in self.vertices_color_dict.keys()]
            return choice(unassigned_variable)
        return heuristic()

    def get_highest_degree_in_graph(self):
        max_length = 0
        for current_vertex in self.graph:
            length = len(self.graph[current_vertex])
            if length > max_length:
                max_length = length
        return max_length

    # remove vertex from both dicts to reset its assignment
    def reset_vertex_assignment(self, vertex):
        self.color_groups_dict[self.vertices_color_dict[vertex]].remove(vertex)
        self.vertices_color_dict.pop(vertex)

    def generate_another_color(self):
        self.color_groups_dict[self.next_color] = []
        self.next_color += 1

    @abstractmethod
    def run(self):
        raise NotImplementedError
