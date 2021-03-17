from StringMatching import StringMatching
from NQueens import NQueens
from random import shuffle, choice


class Chromosome:
    def __init__(self, problem, data=None):
        if data is not None:
            self.data = data
        else:
            self.init_data()
        self.fitness = 0
        self.problem = problem

    def init_data(self):
        target_size = self.problem.get_target_size()
        search_space = self.problem.get_search_space()
        if isinstance(self.problem, NQueens):
            self.data = search_space
            shuffle(self.data)
        elif isinstance(self.problem, StringMatching):
            self.data = list("".join(choice(search_space) for _ in range(target_size)))
