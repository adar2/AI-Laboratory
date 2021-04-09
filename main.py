from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Problems.CVRP import CVRP
from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.GeneticAlgorithm.FitnessFunctions import CVRP_fitness as fitness_func
from Algorithms.GeneticAlgorithm.MatingFunctions import ordered_crossover as mating_func
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation as mutation_func
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection as selection_func
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite as survival_func
from Utils.CVRPFileParsing import parse_cvrp_file, getcwd

# TODO:
# - Add (think about) more Heurisitics
# - Test with all testing files (will probably work)
# - Retest NQueens (OX mating function of GA)
# - Print Correct output with seperation of trucks
# - Excel comparison
# - Lots of BS for the report
# - add to run config


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
    costs = []
    for i in range (20):
        algo = SimpleGeneticAlgorithm(pop_size, max_iter, problem, fitness_func,
                                      mating_func, mutation_func, selection_func, survival_func)
        cost = algo.run()
        costs.append(cost)
    print(costs)
    print(f"Best: {min(costs)}")



