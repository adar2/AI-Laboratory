from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Problems.CVRP import CVRP
from Problems.NQueens import NQueens
from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.GeneticAlgorithm.FitnessFunctions import CVRP_fitness as fitness_func, n_queens_conflicts_fitness as nqueens_fitness
from Algorithms.GeneticAlgorithm.MatingFunctions import ordered_crossover as mating_func
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation as mutation_func
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection as selection_func
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite as survival_func
from Utils.CVRPFileParsing import parse_cvrp_file, getcwd

# TODO:
# - Excel comparison
# - Lots of BS for the report
# - add to run config


if __name__ == '__main__':
    # ***Release Configuration***
    # algo = get_algorithm()
    # algo.run()
    # input('Please press any key to exit...')

    # ***Testing Configuration***
    max_iter = 100
    capacity, locations = parse_cvrp_file(getcwd() + '\E-n101-k14.txt')
    cvrp_problem = CVRP(capacity, locations)
    costs = []

    # CVRP GA Test
    pop_size = 100
    ga_algo = SimpleGeneticAlgorithm(pop_size, max_iter, cvrp_problem, fitness_func,
                                     mating_func, mutation_func, selection_func, survival_func)
    # CVRP Tabu Search Test
    ts_algo = TabuSearch(cvrp_problem,max_iter)
    result = ts_algo.run()
    costs.append(result)
    print(costs)
    print(f"Best: {min(costs)}")



