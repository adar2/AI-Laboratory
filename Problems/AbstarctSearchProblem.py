from abc import ABC, abstractmethod


class AbstractSearchProblem(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_initial_config(self):
        raise NotImplementedError

    @abstractmethod
    def get_sorted_configs(self):
        raise NotImplementedError

    @abstractmethod
    def calc_upper_bound(self, config):
        raise NotImplementedError

    @abstractmethod
    def calc_remaining_capacity(self, config):
        raise NotImplementedError

    @abstractmethod
    def calc_value(self, config):
        raise NotImplementedError

    @abstractmethod
    def expand(self, config) -> list:
        raise NotImplementedError
