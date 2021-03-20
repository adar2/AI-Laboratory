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

    problem = StringMatching("Ronnie And Adar")
    for size in pop_sizes:
        for mutation_rate in mutation_rates:
            for selection_functions in selection_functions:
                for mating_function in mating_functions:


def get_func_name(function):
    name = function.__name__
    name = name.replace('_', ' ')
    print(name)


if __name__ == '__main__':
    sensitivity_comparison()
