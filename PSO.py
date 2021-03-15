import string
from random import random, choice, uniform
import numpy as np
from sys import maxsize
from Particle import Particle
import PSO_constants


class ParticleSwarmOptimization:
    def __init__(self, target_size, fitness_function, population_size):
        self.swarm = self.init_particles()
        self.global_best_position = None
        self.global_best_fitness = maxsize
        self.is_solution_found = False
        self.target_size = target_size
        self.fitness_function = fitness_function
        self.population_size = population_size

    def run(self, max_iterations):
        descending_inertia = np.linspace(0.9, 0.4, max_iterations)
        i = 0
        while i < max_iterations and not self.is_solution_found:
            for particle in self.swarm:
                particle_velocity = self.calculate_particle_velocity(particle, descending_inertia[i])
                particle.update_position(particle_velocity)
                particle.update_fitness()
                self.update_global_best(particle)
                i += 1

    def init_particles(self):
        printable_characters = tuple(c for c in string.printable if c not in ('\t', '\n', '\x0b', '\x0c', '\r'))
        swarm = np.array(
            [Particle(''.join(choice(printable_characters) for _ in range(self.target_size))) for _ in
             range(self.population_size)])
        for particle in swarm:
            particle.update_fitness()
            self.update_global_best(particle)
        return swarm

    def update_global_best(self, particle):
        # if particle.fitness < self.global_best_fitness:
        raise NotImplementedError

    def calculate_particle_velocity(self, particle, current_inertia):
        cognitive_component_random_value = random()
        social_component_random_value = random()
        inertia = current_inertia * particle.velocity
        cognitive_component = PSO_constants.COGNITIVE * cognitive_component_random_value * (particle.personal_best - particle.position)
        social_component = PSO_constants.SOCIAL * social_component_random_value * (self.global_best_position - particle.position)
        return inertia + cognitive_component + social_component
