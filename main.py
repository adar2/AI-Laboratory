from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Problems.CVRP import CVRP
from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.GeneticAlgorithm.FitnessFunctions import CVRP_fitness as fitness_func
from Algorithms.GeneticAlgorithm.MatingFunctions import ordered_crossover as mating_func
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation as mutation_func
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection as selection_func
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite as survival_func
from Utils.CVRPFileParsing import parse_cvrp_file, getcwd

if __name__ == '__main__':
    # ***Release Configuration***
    # algo = get_algorithm()
    # algo.run()
    # input('Please press any key to exit...')

    # ***Testing Configuration***
    pop_size = 100
    max_iter = 100
    capacity, locations = parse_cvrp_file(getcwd() + '\E-n22-k4.txt')
    problem = CVRP(capacity, locations)
    algo = TabuSearch(problem,max_iter)
    algo.run()
