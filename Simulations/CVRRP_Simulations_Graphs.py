from Problems.CVRP import CVRP
from Utils.CVRPFileParsing import parse_cvrp_file, getcwd
from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.LocalSearch.SimulatedAnnealing import SimulatedAnnealing
from Algorithms.ACO.ACO import ACO
from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Algorithms.GeneticAlgorithm.FitnessFunctions import cvrp_fitness as fitness_func
from Algorithms.GeneticAlgorithm.MatingFunctions import partially_matched_crossover as mating_func
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation as mutation_func
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection as selection_func
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite as survival_func


def detect_finding_iteration(lst: list):
    result = 0
    for i in range(1, len(lst)):
        if lst[i] != lst[i - 1]:
            result = i
    return result


def compare_between_iteration_numbers():
    files = ['\E-n22-k4.txt', '\E-n33-k4.txt', '\E-n51-k5.txt', '\E-n76-k8.txt', '\E-n76-k10.txt', '\E-n101-k8.txt',
             '\E-n101-k14.txt']
    iters = [100, 500, 750, 1000]
    aco_file = open("aco_iter_comparison.txt", 'a')
    ts_file = open("ts_iter_comparison.txt", 'a')
    ga_file = open("ga_iter_comparison.txt", 'a')
    sa_file = open("sa_iter_comparison.txt", 'a')
    ga_solutions = []
    ts_solutions = []
    sa_solutions = []
    aco_solutions = []
    for file_index in range(len(files)):
        aco_file.write(f"File: {files[file_index]}\n ------------\n")
        ts_file.write(f"File: {files[file_index]}\n ------------\n")
        ga_file.write(f"File: {files[file_index]}\n ------------\n")
        sa_file.write(f"File: {files[file_index]}\n ------------\n")
        capacity, locations = parse_cvrp_file(getcwd() + files[file_index])
        cvrp_problem = CVRP(capacity, locations)
        for iter_index in range(len(iters)):
            max_iter = iters[iter_index]
            sa_algo = SimulatedAnnealing(cvrp_problem, max_iter)
            sa_algo.run()
            sa_solutions.append(sa_algo.best_config_cost)
            ts_algo = TabuSearch(cvrp_problem, max_iter)
            ts_algo.run()
            ts_solutions.append(ts_algo.best_config_cost)
            aco_algo = ACO(cvrp_problem, max_iter, 25)
            aco_algo.run()
            aco_solutions.append(aco_algo.best_solution[1])
            ga_algo = SimpleGeneticAlgorithm(500, max_iter, cvrp_problem, fitness_func,
                                             mating_func, mutation_func, selection_func, survival_func)
            ga_algo.run()
            ga_solutions.append(ga_algo.best.fitness)
        aco_file.write(f"{aco_solutions}\n")
        ts_file.write(f"{ts_solutions}\n")
        sa_file.write(f"{sa_solutions}\n")
        ga_file.write(f"{ga_solutions}\n")
        aco_solutions.clear()
        ts_solutions.clear()
        sa_solutions.clear()
        ga_solutions.clear()


if __name__ == '__main__':
    compare_between_iteration_numbers()

    # files = ['\E-n22-k4.txt', '\E-n33-k4.txt', '\E-n51-k5.txt', '\E-n76-k8.txt', '\E-n76-k10.txt', '\E-n101-k8.txt',
    #          '\E-n101-k14.txt']
    # for file_index in range(len(files)):
    #     capacity, locations = parse_cvrp_file(getcwd() + files[file_index])
    #     cvrp_problem = CVRP(capacity, locations)
    #     max_iter = 1000
    #     ts_algo = TabuSearch(cvrp_problem, max_iter)
    #     ts_algo.run()
    #     aco_algo = ACO(cvrp_problem, max_iter, 25)
    #     aco_algo.run()
    #     ga_algo = SimpleGeneticAlgorithm(500, max_iter, cvrp_problem, fitness_func,
    #                                      mating_func, mutation_func, selection_func, survival_func)
    #     ga_algo.run()
    #     aco_file = open("aco_summary.txt", 'a')
    #     ts_file = open("ts_summary.txt", 'a')
    #     ga_file = open("ga_summary.txt", 'a')
    #     aco_file.write(f"file: {files[file_index]}\n"
    #                    f"solution: {aco_algo.best_solution[1]} \n"
    #                    f"iterations: {aco_algo.iterations_cost}\n"
    #                    f"number of iterations: {len(aco_algo.iterations_cost)}\n"
    #                    f"last change: {detect_finding_iteration(aco_algo.iterations_cost)}")
    #     ts_file.write(f"file: {files[file_index]}\n "
    #                   f"solution: {ts_algo.best_config_cost}\n"
    #                   f"iterations: {ts_algo.iterations_costs}\n"
    #                   f"number of iterations: {len(ts_algo.iterations_costs)}\n"
    #                   f"last change: {detect_finding_iteration(ts_algo.iterations_costs)}")
    #     ga_file.write(f"file: {files[file_index]}\n "
    #                   f"solution: {ga_algo.best.fitness}\n"
    #                   f"iterations: {ga_algo.iterations_costs}\n"
    #                   f"number of iterations: {ga_algo.number_of_iterations}\n"
    #                   f"last change: {detect_finding_iteration(ga_algo.iterations_costs)}")



    # sa_algo = SimulatedAnnealing(cvrp_problem,max_iter)
    # sa_algo.run()
    # print("^^^^^^^^^^^^^^^^^^^^^^^")
    # print("^^^^^^^^^^^^^^^^^^^^^^^")
    # print(sa_algo.best_config_cost)
    # print(sa_algo.iterations_costs)
    # print(
    #     f"Iterations: {len(sa_algo.iterations_costs)}\n Last Change: Iteration number {detect_finding_iteration(sa_algo.iterations_costs)}")
