from Algorithms.GeneticAlgorithm.GeneticAlgorithmBase import GeneticAlgorithmBase
from Algorithms.GeneticAlgorithm.MatingFunctions import uniform_point_crossover
from Algorithms.GeneticAlgorithm.MutateFunctions import exchange_mutation
from Algorithms.GeneticAlgorithm.NSGAChromosome import NSGAChromosome
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite
from Algorithms.LocalSearch.UtilFunctions import cvrp_path_cost
from Problems.CVRP import CVRP
from Utils.CVRPFileParsing import parse_cvrp_file
from Utils.Constants import MUTATION_RATE, ELITE_RATE


class NSGA2Algorithm(GeneticAlgorithmBase):
    def __init__(self, pop_size, max_iter, problem=None, fitness_function=None, mating_function=uniform_point_crossover,
                 mutation_function=exchange_mutation,
                 selection_function=deterministic_tournament_selection, survival_function=survival_of_the_elite,
                 mutation_rate=MUTATION_RATE, elite_rate=ELITE_RATE):
        super().__init__(pop_size, max_iter, problem, fitness_function, mating_function, mutation_function,
                         selection_function,
                         survival_function, mutation_rate, elite_rate)
        self.fronts = {}

    def init_population(self):
        self.population.clear()
        self.buffer.clear()
        for i in range(self.pop_size):
            chromosome = NSGAChromosome(self.problem)
            self.population.append(chromosome)
        self.buffer = list(self.population)

    def run(self):
        stuck_counter = 0
        self.init_population()
        for i in range(self.max_iter):
            print(f"current iteration : {i + 1}")
            self.calc_fitness()
            self.best = min(self.population, key=lambda chromosome: chromosome.fitness)
            # goal test
            # if self.is_solved_or_stuck(stuck_counter):
            #     self.solved = True
            #     break
            eligible_parents = self.select_parents()
            if eligible_parents is None or len(eligible_parents) == 0:
                continue
            survivors = self.survival_function(self.population, self.elite_rate)
            self.mate(eligible_parents, survivors)
            self.swap()
            self.increase_age()
        return self.best

    # max iter or no improvement
    def is_solved_or_stuck(self, stuck_counter):
        return super().is_solved_or_stuck(stuck_counter)

    # number of fronts, best configuration of smallest front
    def print_current_state(self):
        print("------------------------")
        print(f'Fronts: {len(self.fronts)}')
        print(f'Best = {self.best.data}, from front {self.best.front}')
        print(f'Best stats:\n trucks obj: {self.best.truck_objective} \n route obj: {self.best.route_objectve}')
        print("------------------------")

    # Set front/crowding for each chromosome and then calc its fitness
    def calc_fitness(self):
        # get each objective function value
        self.assign_objective_functions_value()
        # get the front of each chrom
        self.fast_nondominated_sorting()
        # get the crowding of each chrom
        self.assign_crowding_factor()
        # get the fitness of each chrom
        self.assign_objectives_fitness()
        # self.pop = sorted_list
        sorted(self.population, key=lambda chromosome: chromosome.fitness)

    # assign each chromosome with trucks objective and route objective
    def fast_nondominated_sorting(self):
        for chromosome in self.population:

            # reset data structures and fields
            chromosome.dominated_chromosomes_list.clear()
            chromosome.domination_counter = 0
            self.fronts.clear()

            # compare with any other chromosome
            for second_chromosome in self.population:
                # don't compare with yourself
                if chromosome == second_chromosome:
                    continue
                # if this chromosome dominates the second (> = dominates but really it's values are smaller)
                if chromosome > second_chromosome:
                    chromosome.dominated_chromosomes_list.add(second_chromosome)
                elif second_chromosome > chromosome:
                    chromosome.domination_counter += 1
            if chromosome.domination_counter == 0:
                if 1 not in self.fronts:
                    self.fronts[1] = [chromosome]
                else:
                    self.fronts[1].append(chromosome)

        # fill the fronts
        current_front = 1
        while current_front in self.fronts:
            current_front_chromosomes = self.fronts[current_front]
            next_front_chromosomes = []
            for chromosome in current_front_chromosomes:
                chromosome.front = current_front
                for dominated_chromosome in chromosome.dominated_chromosomes_list:
                    dominated_chromosome.domination_counter -= 1
                    if dominated_chromosome.domination_counter == 0:
                        next_front_chromosomes.append(dominated_chromosome)
            if len(next_front_chromosomes) > 0:
                self.fronts[current_front + 1] = next_front_chromosomes
            current_front += 1

    def assign_crowding_factor(self):

        objective_attributes = ['route_objective', 'trucks_objective']

        for chromosome in self.population:
            chromosome.crowding_distance = 0

        for objective in objective_attributes:
            sorted(self.population, key=lambda x: x.__getattribute__(objective))

            self.population[0].crowding_distance = float("inf")
            self.population[len(self.population) - 1].crowding_distance = float("inf")

            for i in range(1, len(self.population) - 1):
                # distance(i) = distance(i) + ((o(i+1) -o(i-1)) / (o(max) -o(min))
                self.population[i].crowding_distance += \
                    (self.population[i + 1].__getattribute__(objective) +
                     self.population[i - 1].__getattribute__(objective)) / \
                    (self.population[len(self.population) - 1].__getattribute__(objective)
                     - self.population[0].__getattribute__(objective))

    # assign a fitness function proportional to both of the objective funtions
    def assign_objectives_fitness(self):
        fitness_counter = 0
        for front in self.fronts.values():
            sorted(front, key=lambda chromosome: chromosome.crowding_distance, reverse=True)
            for chromosome in front:
                chromosome.fitness = fitness_counter
                fitness_counter += 1

    def assign_objective_functions_value(self):
        for chromosome in self.population:
            chromosome.route_objective = cvrp_path_cost(self.problem, chromosome.data)
            chromosome.truck_objective = len(self.problem.generate_truck_partition(chromosome.data))


if __name__ == '__main__':
    capacities, location = parse_cvrp_file('E-n22-k4.txt')
    cvrp_problem = CVRP(capacities, location)
    algo = NSGA2Algorithm(100, 1000, cvrp_problem)
    algo.run()
