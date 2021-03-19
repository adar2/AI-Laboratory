from abc import ABC, abstractmethod


class AbstractProblem(ABC):
    def __init__(self, target, unique=False):
        super().__init__()
        self.target = target
        self.unique = unique

    def get_target_size(self):
        if isinstance(self.target, str) or isinstance(self.target, list) :
            return len(self.target)
        elif isinstance(self.target, int):
            return self.target
        return None

    def get_unique(self):
        return self.unique

    @abstractmethod
    def get_search_space(self):
        raise NotImplementedError
