import random
import time
from math import sqrt
from Problems.KnapSack import KnapSack
from Utils import Constants
from Algorithms.GeneticAlgorithm.Chromosome import Chromosome


class SimpleGeneticAlgorithm:
    def __init__(self, pop_size, max_iter, problem, fitness_function=None,
                 mating_function=None, mutation_function=None, selection_function=None, survival_function=None,
                 mutation_rate=Constants.MUTATION_RATE, elite_rate=Constants.ELITE_RATE):
        # population size
        self.pop_size = pop_size
        # maximum iterations to run
        self.max_iter = max_iter
        # chromosome population list
        self.population = list()
        # chromosome next generation list
        self.buffer = list()
        # best chromosome so far
        self.best = None
        # the search space from which the initial states are constructed from
        self.problem = problem
        # fitness function pointer
        self.fitness_function = fitness_function
        # mating function pointer
        self.mating_function = mating_function
        # mutation function pointer
        self.mutation_function = mutation_function
        # selection function pointer
        self.selection_function = selection_function
        # survival function pointer
        self.survival_function = survival_function
        # number of iterations to complete
        self.number_of_iterations = 0
        # time elapsed from the beginning of run
        self.elapsed_time = 0
        # current time used for calculating the number of ticks of each iteration
        self.current_time = time.time()
        # Denotes whether or not a solution was found
        self.solved = False
        self.mutation_rate = mutation_rate
        self.elite_rate = elite_rate
        self.clock_ticks = 0

    # initialize random chromosomes
    def init_population(self):
        self.population.clear()
        self.buffer.clear()
        for i in range(self.pop_size):
            chromosome = Chromosome(self.problem)
            chromosome.age = random.randint(0, Constants.MAX_RANDOM_AGE)
            if chromosome.age >= Constants.MIN_PARENT_AGE:
                chromosome.fit_to_be_parent = True
            self.population.append(chromosome)
        self.buffer = list(self.population)

    # calculating the fitness of every chromosome in the population
    def calc_fitness(self):
        avg_fitness = 0
        standard_dev = 0
        for chromosome in self.population:
            self.fitness_function(chromosome)
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

    # call mating function to generate the remaining chromosomes for next generation
    def mate(self, eligible_parents, survivors):
        number_of_offsprings = self.pop_size - len(survivors)
        self.buffer = survivors
        for i in range(number_of_offsprings):
            parent_1 = random.choice(eligible_parents)
            parent_2 = random.choice(eligible_parents)
            child = self.mating_function(parent_1, parent_2)
            if random.random() < Constants.MUTATION_RATE:
                self.mutation_function(child)
            self.buffer.append(child)

    # set population as the next generation we've made
    def swap(self):
        temp = self.population
        self.population = self.buffer
        self.buffer = temp

    # returns the number of iterations and time elapsed for each run. used to evaluate statistics.
    def get_stats(self):
        return self.number_of_iterations, self.elapsed_time

    # check whether 90% of the population has the same fitness as optimal solution indicator
    def knapsack_check(self) -> bool:
        fitness_dict = {}
        for chromosome in self.population:
            if chromosome.fitness not in fitness_dict.keys():
                fitness_dict[chromosome.fitness] = 0
            fitness_dict[chromosome.fitness] += 1
        for key in fitness_dict.keys():
            if fitness_dict[key] >= 0.9 * len(self.population):
                return True
        return False

    # run the algorithm until max iter or match was found
    def run(self):
        start_time = time.time()
        self.init_population()
        for i in range(self.max_iter):
            self.number_of_iterations += 1
            self.calc_fitness()
            self.best = min(self.population, key=lambda x: x.fitness)
            print(f'Current Best: {self.problem.printable_data(self.best.data)}')
            print(f'Current Best Fitness: {self.best.fitness}')
            print(f"Clock ticks: {int((time.time() - self.current_time) * Constants.CLOCK_RATE)}")
            self.current_time = time.time()
            # goal test
            if isinstance(self.problem, KnapSack):
                if self.knapsack_check():
                    self.solved = True
                    break
            else:
                if self.best.fitness == 0:
                    self.solved = True
                    break
            eligible_parents = self.select_parents()
            if eligible_parents is None or len(eligible_parents) == 0:
                continue
            survivors = self.survival_function(self.population, self.elite_rate)
            self.mate(eligible_parents, survivors)
            self.swap()
            self.increase_age()
        self.elapsed_time = round(time.time() - start_time, 2)
        self.clock_ticks = self.elapsed_time*Constants.CLOCK_RATE
        print(f"Time elapsed {self.elapsed_time}")
        return self.best

    # select parents using the selection function between all the chromosomes old enough to parent
    def select_parents(self):
        old_enough_to_parent = [c for c in self.population if c.fit_to_be_parent]
        if len(old_enough_to_parent) < 2:
            return None
        return self.selection_function(old_enough_to_parent)

    # increase the age of the population
    def increase_age(self):
        for chromosome in self.population:
            chromosome.grow_old()
