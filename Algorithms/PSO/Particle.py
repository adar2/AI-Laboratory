from copy import deepcopy


class Particle:
    def __init__(self, data, fitness=0):
        # the position of the particle
        self.position = list(ord(c) for c in data)
        # how fit is the data
        self.fitness = fitness
        # particle personal best initiated with its own position
        self.personal_best = deepcopy(self.position)
        # personal best fitness
        self.pb_fitness = fitness
        # particle velocity vector, initiated with None
        self.velocity = None

    def __str__(self):
        return ''.join(chr(i) for i in self.position)

    def __repr__(self):
        return ''.join(chr(i) for i in self.position)
