from StringMatching import StringMatching
from NQueens import NQueens
from random import shuffle, choice
from Constants import MIN_PARENT_AGE


class Chromosome:
    def __init__(self, problem, data=None):
        self.problem = problem
        self.fitness = 0
        self.age = 0
        if data is not None:
            self.data = data
        else:
            self.init_data()
        self.age = 0
        self.fit_to_be_parent = False

    def init_data(self):
        target_size = self.problem.get_target_size()
        search_space = self.problem.get_search_space()
        if isinstance(self.problem, NQueens):
            self.data = search_space
            shuffle(self.data)
        elif isinstance(self.problem, StringMatching):
            self.data = list("".join(choice(search_space) for _ in range(target_size)))

    def grow_old(self):
        self.age += 1
        if self.age >= MIN_PARENT_AGE:
            self.fit_to_be_parent = True
