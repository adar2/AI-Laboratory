from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Problems.CVRP import CVRP
from Problems.NQueens import NQueens
from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.GeneticAlgorithm.FitnessFunctions import cvrp_fitness as fitness_func
from Algorithms.GeneticAlgorithm.MatingFunctions import ordered_crossover as mating_func
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation as mutation_func
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection as selection_func
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite as survival_func
from Utils.CVRPFileParsing import parse_cvrp_file, getcwd
import os
from Utils.Config import get_algorithm

# TODO:
# - Excel comparison
# - Lots of BS for the report

if __name__ == '__main__':
    # ***Release Configuration***
    algo = get_algorithm(os.getcwd())
    algo.run()
    input('Please press any key to exit...')

    # ***Testing Configuration***
    # pop_size = 100
    # max_iter = 100
    # capacity, locations = parse_cvrp_file(getcwd() + '\E-n22-k4.txt')
    # problem = CVRP(capacity, locations)
    # costs = []
    # for i in range(20):
    #     algo = SimpleGeneticAlgorithm(pop_size, max_iter, problem, fitness_func,
    #                                   mating_func, mutation_func, selection_func, survival_func)
    #     cost = algo.run()
    #     costs.append(cost)
    # print(costs)
    # print(f"Best: {min(costs)}")
    # max_iter = 100
    # capacity, locations = parse_cvrp_file(getcwd() + '\E-n101-k14.txt')
    # cvrp_problem = CVRP(capacity, locations)
    # costs = []
    #
    # # CVRP GA Test
    # pop_size = 100
    # ga_algo = SimpleGeneticAlgorithm(pop_size, max_iter, cvrp_problem, fitness_func,
    #                                  mating_func, mutation_func, selection_func, survival_func)
    # # CVRP Tabu Search Test
    # ts_algo = TabuSearch(cvrp_problem,max_iter)
    # result = ts_algo.run()
    # costs.append(result)
    # print(costs)
    # print(f"Best: {min(costs)}")
    # costs = 0
    # algo = get_algorithm(os.getcwd())
    # for i in range(5):
    #     costs += algo.run()[1]
    # print(f"AVG RESULT: {costs/5}")
    # input('Please press any key to exit...')

    # CVRP Simulated Annealing Test
