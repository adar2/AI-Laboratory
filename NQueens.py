from AbstractProblem import AbstractProblem


class NQueens(AbstractProblem):
    def __init__(self, size):
        super().__init__()
        # size is the board size , nxn board has n queens
        self.size = size
        # list of all the numbers [0..size-1]
        self.search_space = list(i for i in range(self.size))

    def get_search_space(self):
        return self.search_space

    def printable_data(self, data: list):
        return ''.join(f'{c},' for c in data)
