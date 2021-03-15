
class Particle:
    def __init__(self, data='', fitness=0):
        self.data = data
        self.fitness = fitness
        self.coordinate_vector = None
        self.personal_best = None
        self.velocity = None

    def calc_coordinate_vector(self):
        self.coordinate_vector = list()
        for char in self.data:
            self.coordinate_vector.append(ord(char))
