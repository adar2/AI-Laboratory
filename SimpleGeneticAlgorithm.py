import random
import string

from Chromosome import Chromosome


class SimpleGeneticAlgorithm:
    def __init__(self, pop_size, max_iter, elite_rate, mutation_rate, target, fitness_function=None,
                 mating_function=None):
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.elite_rate = elite_rate
        self.mutation_rate = mutation_rate
        self.target = target
        self.population = list()
        self.buffer = None
        self.best = None
        self.data = string.printable
        self.fitness_function = fitness_function
        self.mating_function = mating_function

    def init_population(self):
        tsize = len(self.target)
        for i in range(self.pop_size):
            citizen = Chromosome("".join(random.choice(self.data) for _ in range(tsize)), 0)
            self.population.append(citizen)
        self.buffer = list(self.population)

    def calc_fitness(self):
        for citizen in self.population:
            self.fitness_function(citizen, self.target)

    def sort_by_fitness(self):
        self.population.sort(key=lambda x: x.fitness)

    def elitism(self):
        for i in range(0, self.elite_rate * self.pop_size):
            self.buffer.append(self.population[i])

    def mate(self):
        elite_size = int(self.elite_rate * self.pop_size)
        target_size = len(self.target)
        self.mating_function(self.population, self.buffer, elite_size, target_size, self.mutation_rate)

    def swap(self):
        temp = self.population
        self.population = self.buffer
        self.buffer = temp

    def run(self):
        self.init_population()
        for i in range(self.max_iter):
            self.calc_fitness()
            self.sort_by_fitness()
            print(f'Current Best: {self.population[0].data} , {self.population[0].fitness} , {len(self.population[0].data)}')
            if self.population[0].fitness == 0: break
            self.mate()
            self.swap()
