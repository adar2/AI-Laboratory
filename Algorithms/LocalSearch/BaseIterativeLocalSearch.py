from abc import ABC, abstractmethod


class BaseIterativeLocalSearch(ABC):
    def __init__(self, problem, max_iter: int):
        super().__init__()
        self.problem = problem
        self.max_iter = max_iter
        self.current_config = None
        self.current_config_cost = None
        self.best_config = None
        self.proposed_config = None
        self.best_config_cost = None
        self.elapsed_time = None
        self.clock_ticks = None
        self.iterations_costs = []
        self.is_stuck = False
        self.last_config_cost = None
        self.iterations_stuck = 0

    @abstractmethod
    def init_config(self):
        raise NotImplementedError

    @abstractmethod
    def neighbour_config(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def cost(self, config) -> float:
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError
