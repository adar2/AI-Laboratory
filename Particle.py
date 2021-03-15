from copy import deepcopy


class Particle:
    def __init__(self, data, fitness=0):
        self.position = list(ord(c) for c in data)
        self.fitness = fitness
        self.personal_best = deepcopy(self.position)
        self.pb_fitness = fitness
        self.velocity = None

    def __str__(self):
        return ''.join(chr(i) for i in self.position)