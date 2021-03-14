import random
import string
import time
from math import sqrt
from psutil import cpu_freq
from Chromosome import Chromosome


class SimpleGeneticAlgorithm:
    def __init__(self, pop_size, max_iter, elite_rate, mutation_rate, target, fitness_function=None,
                 mating_function=None, number_of_iterations=0, time_elapsed=0):
        # population size
        self.pop_size = pop_size
        # maximum iterations to run
        self.max_iter = max_iter
        # percentage of the top chromosome to copy to next generation
        self.elite_rate = elite_rate
        # probability of chromosome to mutate
        self.mutation_rate = mutation_rate
        # target chromosome
        self.target = target
        # chromosome population list
        self.population = list()
        # chromosome next generation list
        self.buffer = None
        # best chromosome so far
        self.best = None
        # the data from which the initial states are constructed from
        self.data = string.printable
        # fitness function pointer
        self.fitness_function = fitness_function
        # mating function pointer
        self.mating_function = mating_function
        self.number_of_iterations = 0
        self.time_elapsed = 0
        self.current_time = time.time()

    # initialize random chromosomes
    def init_population(self):
        target_size = len(self.target)
        for i in range(self.pop_size):
            chromosome = Chromosome("".join(random.choice(self.data) for _ in range(target_size)), 0)
            self.population.append(chromosome)
        self.buffer = list(self.population)

    # calculating the fitness of every chromosome in the population
    def calc_fitness(self):
        avg_fitness = 0
        standard_dev = 0
        for chromosome in self.population:
            self.fitness_function(chromosome, self.target)
        avg_fitness, standard_dev = self.calc_stats(avg_fitness, standard_dev)
        print(f"Average fitness: {avg_fitness}")
        print(f"Standard Deviation: {standard_dev}")

    # calculate desired stats: currently generational average and standard deviation
    def calc_stats(self, avg_fitness, standard_dev):
        for chromosome in self.population:
            avg_fitness += chromosome.fitness
        avg_fitness /= len(self.population)
        for chromosome in self.population:
            standard_dev += ((chromosome.fitness - avg_fitness) ** 2) / self.pop_size
        standard_dev = sqrt(standard_dev)
        return avg_fitness, standard_dev

    # sorting population by non decreasing fitness
    def sort_by_fitness(self):
        self.population.sort(key=lambda x: x.fitness)

    # copy the first elitism percentage of chromosomes from population to next generation
    def elitism(self):
        for i in range(0, self.elite_rate * self.pop_size):
            self.buffer.append(self.population[i])

    # call mating function to generate the remaining chromosomes for next generation
    def mate(self):
        elite_size = int(self.elite_rate * self.pop_size)
        target_size = len(self.target)
        self.mating_function(self.population, self.buffer, elite_size, target_size, self.mutation_rate)

    # set population as the next generation we've made
    def swap(self):
        temp = self.population
        self.population = self.buffer
        self.buffer = temp

    # returns the number of iterations and time elapsed for each run. used to evaluate statistics.
    def get_stats(self):
        return self.number_of_iterations, self.time_elapsed

    # run the algorithm until max iter or match was found
    def run(self):
        clock_speed = cpu_freq().current * (2 ** 20)
        start_time = time.process_time()
        self.init_population()
        for i in range(self.max_iter):
            self.number_of_iterations += 1
            self.calc_fitness()
            self.sort_by_fitness()
            print(f'Current Best: {self.population[0].data} , {self.population[0].fitness}')
            print(f"Clock ticks: {int((time.time() - self.current_time) * clock_speed)}")
            self.current_time = time.time()
            if self.population[0].fitness == 0:
                break
            self.mate()
            self.swap()
        self.time_elapsed = round(time.process_time() - start_time, 2)
        print(f"Time elapsed {self.time_elapsed}")
