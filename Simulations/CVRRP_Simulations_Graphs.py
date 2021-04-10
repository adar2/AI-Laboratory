from Problems.CVRP import CVRP
from Utils.CVRPFileParsing import parse_cvrp_file, getcwd
from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.LocalSearch.SimulatedAnnealing import SimulatedAnnealing
from Algorithms.ACO.ACO import ACO
from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Algorithms.GeneticAlgorithm.FitnessFunctions import CVRP_fitness as fitness_func
from Algorithms.GeneticAlgorithm.MatingFunctions import ordered_crossover as mating_func
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation as mutation_func
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection as selection_func
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite as survival_func


def detect_finding_iteration(lst: list):
    result = 0
    for i in range(1, len(lst)):
        if lst[i] != lst[i - 1]:
            result = i
    return result


if __name__ == '__main__':
    files = ['\E-n22-k4.txt', '\E-n33-k4.txt', '\E-n51-k5.txt', '\E-n76-k8.txt', '\E-n76-k10.txt', '\E-n101-k8.txt',
             '\E-n101-k14.txt']
    capacity, locations = parse_cvrp_file(getcwd() + files[-1])
    max_iter = 1000
    cvrp_problem = CVRP(capacity, locations)
    ts_algo = TabuSearch(cvrp_problem, max_iter)
    ts_algo.run()
    print("^^^^^^^^^^^^^^^^^^^^^^^")
    print("^^^^^^^^^^^^^^^^^^^^^^^")
    print(ts_algo.best_config_cost)
    print(ts_algo.iterations_costs)
    print(
        f"Iterations: {len(ts_algo.iterations_costs)}\n Last Change: Iteration number {detect_finding_iteration(ts_algo.iterations_costs)}")
