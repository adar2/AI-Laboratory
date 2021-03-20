from random import shuffle, choice, random

from Constants import MIN_PARENT_AGE
from KnapSack import KnapSack
from NQueens import NQueens
from StringMatching import StringMatching


class Chromosome:
    def __init__(self, problem, data=None):
        self.problem = problem
        self.fitness = 0
        self.age = 0
        if data is not None:
            self.data = data
        else:
            self.init_data()
        self.fit_to_be_parent = False

    def init_data(self):
        search_space = self.problem.get_search_space()
        if isinstance(self.problem, NQueens):
            self.data = search_space
            shuffle(self.data)
        elif isinstance(self.problem, StringMatching):
            target_size = self.problem.get_target_size()
            self.data = list("".join(choice(search_space) for _ in range(target_size)))
        elif isinstance(self.problem, KnapSack):
            items = search_space
            self.data = list()
            for _ in items:
                rnd = random()
                if rnd <= 0.5:
                    self.data.append(1)
                else:
                    self.data.append(0)

    def grow_old(self):
        self.age += 1
        if self.age >= MIN_PARENT_AGE:
            self.fit_to_be_parent = True
