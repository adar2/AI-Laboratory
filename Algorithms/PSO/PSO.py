import string
from copy import deepcopy as dc
from random import random, choice, uniform
import time
from Algorithms.PSO.Particle import Particle


class ParticleSwarmOptimization:
    def __init__(self, pop_size, target, inertia_min, inertia_max, c1, c2, max_iter, fitness_function=None):
        # number of particles in the swarm
        self.pop_size = pop_size
        # list of particles
        self.population = list()
        # swarm global best, tuple (global_best_position,global_best_fitness)
        self.global_best = (None, None)
        # search space is printable ascii characters without /t/n/r
        self.search_space = dc(string.printable[:-5])
        # the swarm target
        self.target = target
        # position vector of the target
        self.target_position = list(ord(c) for c in self.target)
        # cognitive constant
        self.cognitive = c1
        # social constant
        self.social = c2
        # maximum inertia
        self.max_inertia = inertia_max
        # minimum inertia
        self.min_inertia = inertia_min
        # initialize the inertia with random number between min and max
        self.inertia = uniform(self.min_inertia, self.max_inertia)
        # maximum iterations
        self.max_iter = max_iter
        # fitness function pointer
        self.fitness_function = fitness_function
        # iterations counter for stats
        self.number_of_iterations = 0
        # time elapsed
        self.time_elapsed = 0

    # initialize swarm particles
    def init_particles(self):
        target_size = len(self.target)
        # delta calculated inorder to initialize particle velocity with random values in range
        delta = abs(ord(self.search_space[0]) - ord(self.search_space[len(self.search_space) - 1]))
        for i in range(self.pop_size):
            particle = Particle("".join(choice(self.search_space) for _ in range(target_size)))
            self.fitness_function(particle, self.target_position)
            particle.velocity = list(int(uniform(-delta, delta)) for _ in range(target_size))
            particle.pb_fitness = dc(particle.fitness)
            self.population.append(particle)
        # sort by fitness and set global best
        self.population.sort(key=lambda x: x.fitness)
        self.global_best = (dc(self.population[0].position), dc(self.population[0].fitness))

    def run(self):
        start_time = time.time()
        target_size = len(self.target)
        self.init_particles()
        for i in range(self.max_iter):
            self.number_of_iterations = i
            print(f"Current Best {self.global_best[0]} {self.global_best[1]}")
            # calculate new position for each particle according to the formula
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
                self.time_elapsed = time.time() - start_time

            if self.global_best[1] == 0:
                break
            if self.inertia > self.min_inertia:
                self.inertia -= .01
