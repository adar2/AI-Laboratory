from AbstractProblem import AbstractProblem


class NQueens(AbstractProblem):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.search_space = list(i for i in range(self.size))

    def get_search_space(self):
        return self.search_space
