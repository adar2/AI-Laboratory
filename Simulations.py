# String Matching
# Parameters:
# - Population Size
# - Mutation Rate
# - Elite Rate
# - Selection Function
# - Survival Function
# - Mating Function
# - Mutation Function
from Constants import MUTATION_RATE, ELITE_RATE
from SurvivalFunctions import survival_of_the_elite, survival_of_the_young
from GeneticAlgorithm import SimpleGeneticAlgorithm
from MutateFunctions import string_mutation
from MatingFunctions import single_point_crossover, uniform_point_crossover, multi_point_crossover
from StringMatching import StringMatching
from FitnessFunctions import bullseye_fitness
import SelectionFunctions
from matplotlib import pyplot as plt


def plot_and_show_iterations(number_of_runs, number_of_iterations_PSO, number_of_iterations_GA):
    plt.plot(number_of_runs, number_of_iterations_PSO)
    plt.plot(number_of_runs, number_of_iterations_GA)
    plt.xlabel("Runs")
    plt.ylabel("Iterations")
    plt.title("Comparison of PSO and GA performance")
    plt.legend(['PSO', 'GA'])
    plt.show()


def sensitivity_comparison():
    pop_sizes = [256, 512, 1024, 2048, 4096, 8192]
    mutation_rates = [0.25, 0.5, 0.75]
    selection_functions = [SelectionFunctions.truncation_selection, SelectionFunctions.stochastic_tournament_selection,
                           SelectionFunctions.deterministic_tournament_selection, SelectionFunctions.rws, SelectionFunctions.sus]
    mating_functions = [single_point_crossover, multi_point_crossover, uniform_point_crossover]
    survival_functions = [survival_of_the_elite, survival_of_the_young]
    elite_rates = [0.6, 0.8, 0.9]

    problem = StringMatching("Ronnie And Adar")
    success_dict = {}
    for size in pop_sizes:
        for mutation_rate in mutation_rates:
            for selection_function in selection_functions:
                for mating_function in mating_functions:
                    for survival_function in survival_functions:
                        for elite_rate in elite_rates:
                            algo = SimpleGeneticAlgorithm(size, 16000, problem, bullseye_fitness,
                                                          mating_function, string_mutation, selection_function, survival_function,
                                                          mutation_rate, elite_rate)
                            iterations_performance = []
                            runtime_performance = []
                            success_counter = 0
                            for i in range(10):
                                algo.run()
                                if algo.solved:
                                    success_counter += 1
                                    iterations, time = algo.get_stats()
                                    iterations_performance.append(iterations)
                                    runtime_performance.append(time)
                            plot_results(size, mating_function, selection_function, survival_function, mutation_rate, elite_rate, iterations_performance, runtime_performance, success_counter)





def get_func_name(function):
    name = function.__name__
    name = name.replace('_', ' ')
    print(name)


if __name__ == '__main__':
    sensitivity_comparison()
