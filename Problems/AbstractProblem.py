from abc import ABC, abstractmethod


class AbstractProblem(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_search_space(self):
        raise NotImplementedError

    @abstractmethod
    def printable_data(self, data: list):
        raise NotImplementedError
