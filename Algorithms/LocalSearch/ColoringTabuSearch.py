from Problems.AbstractProblem import AbstractProblem
from Problems.GraphColoringProblem import GraphColoringProblem
from TabuSearch import TabuSearch
from UtilFunctions import coloring_init_config


class ColoringTabuSearch(TabuSearch):
    def __init__(self, problem: GraphColoringProblem, max_iter: int):
        super().__init__(problem, max_iter)

    # get neighbours
    def neighbour_config(self) -> list:
        pass

    # greedy algorithm for base config
    def init_config(self):
        return coloring_init_config(self.problem)

    # Objective function (likely to vary between the 3 options)
    def cost(self, config) -> float:
        pass
