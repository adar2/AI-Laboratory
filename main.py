from matplotlib import pyplot as plt
from NQueens import NQueens
from FitnessFunctions import pso_distance_fitness as absolute, bullseye_fitness as bullseye, \
    n_queens_conflicts_fitness as nqueens_fitness
from MatingFunctions import ordered_crossover as mating_func
from MutateFunctions import insertion_mutation as mutation_func
from SelectionFunctions import deterministic_tournament_selection as selection_func
from SurvivalFunctions import survival_of_the_elite as survival_func
from GeneticAlgorithm import SimpleGeneticAlgorithm
from PSO import ParticleSwarmOptimization
from StringMatching import StringMatching
from Chromosome import Chromosome
from copy import copy
from Config import get_algorithm


def run_and_plot():
    number_of_runs = range(10)
    number_of_iterations_a = []
    number_of_iterations_b = []
    algo_time_a = []
    algo_time_b = []
    for i in range(10):
        bullseye_algo = SimpleGeneticAlgorithm(2048, 16384, .1, .25, "Hello world!", bullseye,
                                               mating_func)
        abs_algo = SimpleGeneticAlgorithm(2048, 16384, .1, .25, "Hello world!", absolute,
                                          mating_func)
        abs_algo.run()
        a_iterations, a_time = abs_algo.get_stats()
        algo_time_a.append(a_time)
        number_of_iterations_a.append(a_iterations)

        bullseye_algo.run()
        b_iterations, b_time = bullseye_algo.get_stats()
        algo_time_b.append(b_time)
        number_of_iterations_b.append(b_iterations)
    plt.plot(number_of_runs, algo_time_a)
    plt.plot(number_of_runs, algo_time_b)
    plt.xlabel("Runs")
    plt.ylabel("Time to complete (secs)")
    plt.title("Comparison of Bullseye and Absolute Distance Fitness Functions")
    plt.legend(['Absolute Distance', 'Bullseye'])
    plt.show()


def plot_compare_pso_GA():
    number_of_runs = range(10)
    number_of_iterations_GA = []
    number_of_iterations_PSO = []
    algo_time_GA = []
    algo_time_PSO = []
    for i in range(10):
        bullseye_algo = SimpleGeneticAlgorithm(2048, 16384, .1, .25, "Hello world!", bullseye,
                                               mating_func)
        p = ParticleSwarmOptimization(2048, "Hello world!", .4, .9, 2, 2, 300, absolute)
        p.run()
        bullseye_algo.run()
        GA_iterations, GA_time = bullseye_algo.get_stats()
        PSO_iterations = p.number_of_iterations
        PSO_time = p.time_elapsed
        number_of_iterations_PSO.append(PSO_iterations)
        number_of_iterations_GA.append(GA_iterations)
        algo_time_PSO.append(PSO_time)
        algo_time_GA.append(GA_time)

    plot_and_show_iterations(number_of_runs, number_of_iterations_PSO, number_of_iterations_GA)
    plot_and_show_time(number_of_runs, algo_time_PSO, algo_time_GA)


def plot_and_show_time(number_of_runs, algo_time_PSO, algo_time_GA):
    plt.plot(number_of_runs, algo_time_PSO)
    plt.plot(number_of_runs, algo_time_GA)
    plt.xlabel("Runs")
    plt.ylabel("Time of run (secs)")
    plt.title("Comparison of PSO and GA performance")
    plt.legend(['PSO', 'GA'])
    plt.show()


def plot_and_show_iterations(number_of_runs, number_of_iterations_PSO, number_of_iterations_GA):
    plt.plot(number_of_runs, number_of_iterations_PSO)
    plt.plot(number_of_runs, number_of_iterations_GA)
    plt.xlabel("Runs")
    plt.ylabel("Iterations")
    plt.title("Comparison of PSO and GA performance")
    plt.legend(['PSO', 'GA'])
    plt.show()


def mutation_test(problem_type):
    for i in range(10):
        problem = problem_type(range(10))
        chrom = Chromosome(problem)
        before = copy(chrom.data)
        mutation_func(chrom)
        after = chrom.data
        print(f'{before} -> {after}, len={len(after)}')


def mating_test(problem_type):
    for i in range(10):
        problem = problem_type(range(10))
        chrom_1 = Chromosome(problem)
        chrom_2 = Chromosome(problem)
        child = mating_func(chrom_1, chrom_2)
        print(f'{chrom_1.data} + {chrom_2.data} = {child.data}, len={len(child.data)}')


if __name__ == '__main__':
    # plot_compare_pso_GA()
    # success_counter = 0
    # for i in range(5):
    #     problem = NQueens([1, 2, 3, 4, 5, 6, 7, 8])
    #     algo = SimpleGeneticAlgorithm(2048, 16384, problem, nqueens_fitness,
    #                                   mating_func, mutation_func, selection_func, survival_func)
    #     algo.run()
    #     if algo.solved:
    #         success_counter += 1
    # print(f"Success = {success_counter}")
    algo = get_algorithm()
    algo.run()
