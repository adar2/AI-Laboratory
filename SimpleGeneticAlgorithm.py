from Chromosome import Chromosome
import random
import string


class SimpleGeneticAlgorithm:
    def __init__(self, pop_size, max_iter, elite_rate, mutation_rate, target,fitness_function=None,mating_function=None):
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.elite_rate = elite_rate
        self.mutation_rate = mutation_rate
        self.target = target
        self.population = list()
        self.buffer = list()
        self.best = None
        self.data = string.printable
        self.fitness_function = fitness_function
        self.mating_function = mating_function

    def init_population(self):
        tsize = len(self.target) - 1
        for i in range(0, self.pop_size - 1):
            citizen = Chromosome("".join(random.choice(self.data) for _ in range(0, tsize)), 0)
            self.population.append(citizen)

    def calc_fitness(self):
        for citizen in self.population:
            self.fitness_function(citizen)

    def sort_by_fitness(self):
        self.population.sort(key=lambda x : x.fitness)

    def elitism(self):
        for i in range(0,self.elite_rate*self.pop_size):
            self.buffer.append(self.population[i])

    def mutate(self):
        elite_size = self.elite_rate*self.pop_size
        target_size = len(self.target)
        self.mating_function(self.population, self.buffer, elite_size, target_size, self.mutation_rate)

    def mate(self):
        pass