from AbstractProblem import AbstractProblem
import string


class StringMatching(AbstractProblem):
    def __init__(self, target):
        super().__init__(target, False)
        # remove /t/n/r
        self.search_space = list(string.printable[:-5])

    def get_search_space(self):
        return self.search_space
