import random
import time
from abc import abstractmethod
from math import sqrt

from Algorithms.GeneticAlgorithm.Chromosome import Chromosome
from Utils.Constants import MUTATION_RATE, ELITE_RATE, STUCK_PCT, MAX_RANDOM_AGE, MIN_PARENT_AGE, CLOCK_RATE


class GeneticAlgorithmBase:
    def __init__(self, pop_size, max_iter, problem=None, fitness_function=None,
                 mating_function=None, mutation_function=None, selection_function=None, survival_function=None,
                 mutation_rate=MUTATION_RATE, elite_rate=ELITE_RATE):
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
        self.iterations_costs = []

    # initialize random chromosomes
    def init_population(self):
        self.population.clear()
        self.buffer.clear()
        for i in range(self.pop_size):
            chromosome = Chromosome(self.problem)
            chromosome.age = random.randint(0,MAX_RANDOM_AGE)
            if chromosome.age >= MIN_PARENT_AGE:
                chromosome.fit_to_be_parent = True
            self.population.append(chromosome)
        self.buffer = list(self.population)

    # calculating the fitness of every chromosome in the population
    def calc_fitness(self):
        avg_fitness = 0
        standard_dev = 0
        for chromosome in self.population:
            self.fitness_function(chromosome)
        # avg_fitness, standard_dev = self.calc_stats(avg_fitness, standard_dev)
        # print(f"Average fitness: {avg_fitness}")
        # print(f"Standard Deviation: {standard_dev}")

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
            if random.random() < MUTATION_RATE:
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
    @abstractmethod
    def run(self):
        raise NotImplementedError

    def update_time_stats(self, start_time):
        self.elapsed_time = round(time.time() - start_time, 2)
        self.clock_ticks = self.elapsed_time * CLOCK_RATE

    def is_solved_or_stuck(self, stuck_counter):
        return self.best.fitness == 0 or (stuck_counter / self.max_iter) >= STUCK_PCT

    def update_stuck_counter(self, last_best, stuck_counter):
        if last_best is None:
            last_best = self.best.fitness
        if last_best == self.best.fitness:
            stuck_counter += 1
        else:
            last_best = self.best.fitness
            stuck_counter = 0
        return stuck_counter, last_best

    def print_current_state(self):
        print(f'Current Best: {self.problem.printable_data(self.best.data)}')
        print(f'Current Best Fitness: {self.best.fitness}')
        print(f"Clock ticks: {int((time.time() - self.current_time) * CLOCK_RATE)}")

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
