from matplotlib import pyplot as plt

from FitnessFunctions import distance_fitness as absolute
from FitnessFunctions import bullseye_fitness as bullseye
from MatingFunctions import single_point_crossover as mating_func
from SimpleGeneticAlgorithm import SimpleGeneticAlgorithm
from PSO import ParticleSwarmOptimization


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


if __name__ == '__main__':
    # run_and_plot()
    p = ParticleSwarmOptimization(30, "Hello world!", .4, .9, 2, 2, 2000, absolute)
    p.run()
