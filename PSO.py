import string
from copy import deepcopy as dc
from random import random, choice, uniform
from time import process_time

from Particle import Particle


class ParticleSwarmOptimization:
    def __init__(self, pop_size, target, inertia_min, inertia_max, c1, c2, max_iter, fitness_function=None):
        self.pop_size = pop_size
        self.population = list()
        self.global_best = (None, None)
        self.data = dc(string.printable[:-6])
        self.target = target
        self.target_position = list(ord(c) for c in self.target)
        self.cognitive = c1
        self.social = c2
        self.max_inertia = inertia_max
        self.min_inertia = inertia_min
        self.inertia = uniform(self.min_inertia, self.max_inertia)
        self.max_iter = max_iter
        self.fitness_function = fitness_function
        self.number_of_iterations = 0
        self.time_elapsed = 0

    def init_particles(self):
        target_size = len(self.target)
        delta = abs(ord(self.data[0]) - ord(self.data[len(self.data) - 1]))
        for i in range(self.pop_size):
            particle = Particle("".join(choice(self.data) for _ in range(target_size)))
            self.fitness_function(particle, self.target_position)
            particle.velocity = list(int(uniform(-delta, delta)) for _ in range(target_size))
            particle.pb_fitness = dc(particle.fitness)
            self.population.append(particle)
        self.population.sort(key=lambda x: x.fitness)
        self.global_best = (dc(self.population[0].position), dc(self.population[0].fitness))

    def run(self):
        start_time = process_time()
        target_size = len(self.target)
        self.init_particles()
        for i in range(self.max_iter):
            self.number_of_iterations = i
            print(f"Current Best {self.global_best[0]} {self.global_best[1]}")
            for j in range(len(self.population)):
                particle = self.population[j]
                for dimension in range(target_size):
                    r1 = random()
                    r2 = random()
                    personal_best_delta = (particle.personal_best[dimension] - particle.position[dimension])
                    global_best_delta = (self.global_best[0][dimension] - particle.position[dimension])
                    particle.velocity[dimension] = self.inertia * particle.velocity[dimension] + \
                                                   self.cognitive * r1 * personal_best_delta + \
                                                   self.social * r2 * global_best_delta
                    particle.position[dimension] += int(random() * particle.velocity[dimension])
                self.fitness_function(particle, self.target_position)
                fitness = particle.fitness
                if fitness < particle.pb_fitness:
                    particle.pb_fitness = dc(fitness)
                    particle.personal_best = dc(particle.position)
                    if fitness < self.global_best[1]:
                        self.global_best = (dc(particle.position), dc(fitness))
                self.time_elapsed = process_time() - start_time

            if self.global_best[1] == 0:
                break
            if self.inertia > self.min_inertia:
                self.inertia -= .01
