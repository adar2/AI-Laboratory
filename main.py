from matplotlib import pyplot as plt

from FitnessFunctions import distance_fitness as absolute
from FitnessFunctions import bullseye_fitness as bullseye
from MatingFunctions import single_point_crossover as mating_func
from MutateFunctions import string_mutation as mutation_func
from SelectionFunctions import truncation_selection as selection_func
from SimpleGeneticAlgorithm import SimpleGeneticAlgorithm
from PSO import ParticleSwarmOptimization
from StringMatching import StringMatching


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


if __name__ == '__main__':
    # plot_compare_pso_GA()
    problem = StringMatching("Hello world!")
    bullseye_algo = SimpleGeneticAlgorithm(2048, 16384, problem, bullseye,
                                           mating_func, mutation_func, selection_func)
    bullseye_algo.run()
