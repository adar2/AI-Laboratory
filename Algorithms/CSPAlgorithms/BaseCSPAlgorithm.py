from abc import ABC, abstractmethod
from Problems.AbstractProblem import AbstractProblem


class BaseCSPAlgorithm(ABC):

    def __init__(self, problem: AbstractProblem) -> None:
        super().__init__()
        self.graph = problem.get_search_space()
        self.constraints_dict = problem.get_search_space()
        self.current_color = 1
        self.color_groups_dict = {}  # 1: [5,4,1] 2: 6,7,8
        self.vertices_color_dict = {}  # 1:2

    def update_vertex(self, vertex: int, color: int):
        if self.vertices_color_dict[vertex] is not None:
            self.color_groups_dict[self.vertices_color_dict[vertex]].remove(vertex)
        self.vertices_color_dict[vertex] = color
        self.color_groups_dict[color].append(vertex)

    @abstractmethod
    def run(self):
        raise NotImplementedError
