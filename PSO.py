import string
from random import random, choice, uniform

from Particle import Particle


class ParticleSwarmOptimization:
    def __init__(self, pop_size, target, inertia_min, inertia_max, c1, c2, max_iter, fitness_function=None):
        self.pop_size = pop_size
        self.population = list()
        self.global_best = Particle()
        self.data = string.printable
        self.target = target
        self.target_coordinate_vector = list(ord(self.target[i]) for i in range(len(self.target)))
        self.c1 = c1
        self.c2 = c2
        self.inertia_max = inertia_max
        self.inertia_min = inertia_min
        self.inertia = uniform(self.inertia_min, self.inertia_max)
        self.max_iter = max_iter
        self.fitness_function = fitness_function

    def init_particles(self):
        target_size = len(self.target)
        delta = abs(ord(self.data[0]) - ord(self.data[len(self.data) - 1]))
        for i in range(self.pop_size):
            particle = Particle("".join(choice(self.data) for _ in range(target_size)))
            particle.calc_coordinate_vector()
            self.fitness_function(particle, self.target_coordinate_vector)
            particle.personal_best = Particle(particle.data, particle.fitness)
            particle.personal_best.calc_coordinate_vector()
            particle.velocity = list(int(uniform(-delta, delta)) for _ in range(target_size))
            self.population.append(particle)
        self.population.sort(key=lambda x: x.fitness)
        self.global_best.data = self.population[0].data
        self.global_best.fitness = self.population[0].fitness
        self.global_best.calc_coordinate_vector()

    def run(self):
        target_size = len(self.target)
        self.init_particles()
        for i in range(self.max_iter):
            print(f"Current Best {self.global_best.data} {self.global_best.fitness}")
            for particle in self.population:
                for dimension in range(target_size):
                    particle.velocity[dimension] = self.inertia * particle.velocity[dimension] + \
                                                   self.c1 * random() * (
                                                           particle.personal_best.coordinate_vector[dimension]
                                                           - particle.coordinate_vector[dimension]) + \
                                                   self.c2 * random() * (self.global_best.coordinate_vector[dimension] -
                                                                         particle.coordinate_vector[dimension])
                    particle.coordinate_vector[dimension] = (particle.coordinate_vector[dimension] + int(
                        random() * particle.velocity[dimension])) % 127
                    if particle.coordinate_vector[dimension] < 32:
                        particle.coordinate_vector[dimension] = particle.coordinate_vector[dimension] + (
                                    32 - particle.coordinate_vector[dimension])
                self.fitness_function(particle, self.target_coordinate_vector)
                fitness = particle.fitness
                if fitness < particle.personal_best.fitness:
                    particle.personal_best.fitness = fitness
                    particle.personal_best.data = particle.data
                    particle.personal_best.calc_coordinate_vector()
                    if fitness < self.global_best.fitness:
                        self.global_best.data = particle.data
                        self.global_best.fitness = fitness
                        self.global_best.calc_coordinate_vector()

            if self.global_best.fitness == 0:
                break
            if self.inertia > self.inertia_min:
                self.inertia -= .01
