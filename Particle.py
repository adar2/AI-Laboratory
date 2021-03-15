import numpy as np
from random import randint
from PSO_constants import NUMBER_OF_POSSIBLE_CHARACTERS


class Particle:
    def __init__(self, data='', fitness=0):
        self.data = data
        self.fitness = fitness
        self.position = self.calc_position()
        self.personal_best = np.copy(self.position)
        self.velocity = np.array(
            [randint(-NUMBER_OF_POSSIBLE_CHARACTERS, NUMBER_OF_POSSIBLE_CHARACTERS) for _ in
             self.data])

    def calc_position(self):
        return np.array([ord(char) for char in self.data])
