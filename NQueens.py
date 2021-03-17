from AbstractProblem import AbstractProblem


class NQueens(AbstractProblem):
    def __init__(self, target):
        super().__init__(target, True)
        self.search_space = list(i for i in range(1, self.get_target_size() + 1))

    def get_search_space(self):
        return self.search_space
