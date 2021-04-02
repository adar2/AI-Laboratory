from Config import get_algorithm
from GeneticAlgorithm import SimpleGeneticAlgorithm
from CVRP import CVRP
from FitnessFunctions import CVRP_fitness as fitness_func
from MatingFunctions import partially_matched_crossover as mating_func
from MutateFunctions import exchange_mutation as mutation_func
from SelectionFunctions import truncation_selection as selection_func
from SurvivalFunctions import survival_of_the_elite as survival_func

if __name__ == '__main__':
    # ***Release Configuration***
    # algo = get_algorithm()
    # algo.run()
    # input('Please press any key to exit...')

    # ***Testing Configuration***
    pop_size = 100
    max_iter = 100
    problem = CVRP(10, [((0, 0), 0), ((0, 10), 3), ((-10, 10,), 3), ((0,-10),3),((10,-10),3)])

    algo = SimpleGeneticAlgorithm(pop_size, max_iter, problem, fitness_func,
                                  mating_func, mutation_func, selection_func, survival_func)
    algo.run()
