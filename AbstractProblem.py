from abc import ABC, abstractmethod


class AbstractProblem(ABC):
    def __init__(self, target, unique=False):
        super().__init__()
        self.target = target
        self.unique = unique

    def get_target_size(self):
        if self.target is not None:
            return len(self.target)
        return None

    def get_unique(self):
        return self.unique

    @abstractmethod
    def get_search_space(self):
        raise NotImplementedError
