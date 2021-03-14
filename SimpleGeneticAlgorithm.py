import random
import string
import time
from psutil import cpu_freq
from Chromosome import Chromosome


class SimpleGeneticAlgorithm:
    def __init__(self, pop_size, max_iter, elite_rate, mutation_rate, target, fitness_function=None,
                 mating_function=None):
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
        # average fitness value of all the chromosomes
        self.avg_fitness = 0

        self.current_time = time.time()

    # initialize random chromosomes
    def init_population(self):
        target_size = len(self.target)
        for i in range(self.pop_size):
            chromosome = Chromosome("".join(random.choice(self.data) for _ in range(target_size)), 0)
            self.population.append(chromosome)
        self.buffer = list(self.population)

    # calculating the fitness of every chromosome in the population and the average fitness
    def calc_fitness(self):
        self.avg_fitness = 0
        for chromosome in self.population:
            self.fitness_function(chromosome, self.target)
            self.avg_fitness += chromosome.fitness
        self.avg_fitness /= len(self.population)
        print(f"Avg fitness {self.avg_fitness}")

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

    # run the algorithm until max iter or match was found
    def run(self):
        clock_speed = cpu_freq().current * (2 ** 20)
        self.init_population()
        for i in range(self.max_iter):
            self.calc_fitness()
            self.sort_by_fitness()
            print(f'Current Best: {self.population[0].data} , {self.population[0].fitness}')
            print(f"Clock ticks {int((time.time() - self.current_time) * clock_speed)}")
            self.current_time = time.time()
            if self.population[0].fitness == 0:
                break
            self.mate()
            self.swap()
        time_elapsed = time.process_time()
        print(f"Time elapsed {time_elapsed}")
