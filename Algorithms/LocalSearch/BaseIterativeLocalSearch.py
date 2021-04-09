from abc import ABC, abstractmethod
from Problems.AbstractProblem import AbstractProblem
from Utils.UtilFunctions import euc_distance, cvrp_path_cost
from Utils.Constants import DEMAND, COORDINATES


class BaseIterativeLocalSearch(ABC):
    def __init__(self, problem: AbstractProblem, max_iter: int):
        super().__init__()
        self.problem = problem
        self.max_iter = max_iter
        self.current_config = None
        self.current_config_cost = None
        self.best_config = None
        self.proposed_config = None
        self.best_config_cost = None

    def init_config(self):
        config = []
        search_space = self.problem.get_search_space()
        current_location = search_space[0]
        search_space = search_space[1:]
        config.append(current_location)
        while search_space:
            min_location = None
            min_location_distance = 0
            for location in search_space:
                distance = euc_distance(current_location[COORDINATES], location[COORDINATES])
                if min_location is None or distance < min_location_distance:
                    min_location = location
                    min_location_distance = distance
            current_location = min_location
            config.append(current_location)
            search_space.remove(current_location)
        return config

    @abstractmethod
    def neighbour_config(self) -> list:
        raise NotImplementedError

    def cost(self, config) -> float:
        return cvrp_path_cost(self.problem, config)

    @abstractmethod
    def run(self):
        raise NotImplementedError
