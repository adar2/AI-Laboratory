from abc import ABC, abstractmethod

class BaseIterativeLocalSearch(ABC):

    def __init__(self, graph_dict: dict) -> None:
        super().__init__()
        self.graph = graph_dict
        self.constraints_dict = graph_dict
        self.current_color = 1
        self.color_groups_dict = {}

    @abstractmethod
    def run(self):








