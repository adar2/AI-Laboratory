# String Matching
# Parameters:
# - Population Size
# - Mutation Rate
# - Elite Rate
# - Selection Function
# - Survival Function
# - Mating Function
# - Mutation Function
from SimulationResult import SimulationResult
from SurvivalFunctions import survival_of_the_elite, survival_of_the_young
from GeneticAlgorithm import SimpleGeneticAlgorithm
from MutateFunctions import string_mutation, inversion_mutation, exchange_mutation, insertion_mutation, displacement_mutation
from MatingFunctions import single_point_crossover, uniform_point_crossover, multi_point_crossover, ordered_crossover, \
    partially_matched_crossover
from StringMatching import StringMatching
from NQueens import NQueens
from FitnessFunctions import bullseye_fitness, n_queens_conflicts_fitness
import SelectionFunctions
from matplotlib import pyplot as plt
from statistics import mean
import xlwt


def plot_and_show_iterations(number_of_runs, number_of_iterations_PSO, number_of_iterations_GA):
    plt.plot(number_of_runs, number_of_iterations_PSO)
    plt.plot(number_of_runs, number_of_iterations_GA)
    plt.xlabel("Runs")
    plt.ylabel("Iterations")
    plt.title("Comparison of PSO and GA performance")
    plt.legend(['PSO', 'GA'])
    plt.show()


def plot_and_show_single(y_axis_parameter, size, mating_function, selection_function, survival_function, mutation_rate, elite_rate,
                         performance_list):
    runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.plot(runs, performance_list)
    plt.xlabel("Runs")
    plt.ylabel(y_axis_parameter)
    plt.title(
        f'{y_axis_parameter} performance of size={size}, mating strategy={get_func_name(mating_function)}, selection strategy = {get_func_name(selection_function)}, survival strategy = {get_func_name(survival_function)}, mutation rate = {mutation_rate}, elite pct = {elite_rate}')
    plt.show()


def plot_list_iterations(results_list):
    runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for result in results_list:
        plt.plot(runs, result.iterations_data)
    plt.xlabel("Runs")
    plt.ylabel("Iterations")
    plt.legend(["Best", "Second", "Third"])
    plt.title("Comparison of the top 3 configurations by iterations count")
    plt.show()


def plot_list_runtime(results_list):
    runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for result in results_list:
        plt.plot(runs, result.runtime_data)
    plt.xlabel("Runs")
    plt.ylabel("Runtime")
    plt.legend(["Best", "Second", "Third"])
    plt.title("Comparison of the top 3 configurations by runtime")
    plt.show()


def plot_results_list(Y_axis_parameter, results_list):
    if Y_axis_parameter == "Iterations":
        plot_list_iterations(results_list)
    else:
        plot_list_runtime(results_list)


def add_results_to_sheet(stats, line, size, mating_function, selection_function, survival_function, mutation_rate, elite_rate,
                         iterations_performance, runtime_performance, success_counter):
    stats.write(line, 0, "String Matching")
    stats.write(line, 1, size)
    stats.write(line, 2, mutation_rate)
    stats.write(line, 3, elite_rate)
    stats.write(line, 4, get_func_name(selection_function))
    stats.write(line, 5, get_func_name(mating_function))
    stats.write(line, 6, get_func_name(survival_function))
    stats.write(line, 7, f"{success_counter * 10}%")
    stats.write(line, 8, round(mean(iterations_performance), 2))
    stats.write(line, 9, round(mean(runtime_performance), 2))


def update_best(result, best_runtime, best_iterations):
    if len(best_runtime) < 3:
        best_runtime.append(result)
    else:
        max_runtime = max(best_runtime, key=lambda x: x.runtime_mean)
        if result.runtime_mean < max_runtime.runtime_mean:
            best_runtime.remove(max_runtime)
            best_runtime.append(result)

    if len(best_iterations) < 3:
        best_iterations.append(result)
    else:
        max_iterations = max(best_iterations, key=lambda x: x.iterations_mean)
        if result.runtime_mean < max_iterations.runtime_mean:
            best_iterations.remove(max_iterations)
            best_iterations.append(result)


def print_results(results_list):
    i = 1
    for result in results_list:
        print(f"Number {i}:")
        print(result)
        i += 1


def create_simulation_report():
    # prepare run parameters
    pop_sizes = [256, 512, 1024]
    mutation_rates = [0.25, 0.5, 0.75]
    selection_functions = [SelectionFunctions.truncation_selection, SelectionFunctions.stochastic_tournament_selection,
                           SelectionFunctions.roulette_wheel_selection, SelectionFunctions.stochastic_universal_sampling_selection]
    mating_functions = [ordered_crossover, partially_matched_crossover]
    mutation_functions = [exchange_mutation, insertion_mutation, inversion_mutation, displacement_mutation]
    survival_functions = [survival_of_the_elite, survival_of_the_young]
    elite_rates = [0.6, 0.8, 0.9]
    problem = NQueens(8)

    # prepare excel workbook
    workbook = xlwt.Workbook()
    stats = workbook.add_sheet('NQueens_Stats')
    stats.write(0, 0, 'Algorithm')
    stats.write(0, 1, 'Population Size')
    stats.write(0, 2, 'Mutation Rate')
    stats.write(0, 3, 'Elite Pct.')
    stats.write(0, 4, 'Selection Strategy')
    stats.write(0, 5, 'Mating Strategy')
    stats.write(0, 6, 'Survival Strategy')
    stats.write(0, 7, 'Success Pct.')
    stats.write(0, 8, 'Average Iterations')
    stats.write(0, 9, 'Average Runtime')
    current_line = 1

    # prepare bests
    best_runtime = []
    best_iterations = []

    # simulations
    for size in pop_sizes:
        for mutation_rate in mutation_rates:
            for selection_function in selection_functions:
                for mating_function in mating_functions:
                    for mutation_function in mutation_functions:
                        for survival_function in survival_functions:
                            for elite_rate in elite_rates:
                                algo = SimpleGeneticAlgorithm(size, 16000, problem, n_queens_conflicts_fitness,
                                                              mating_function, mutation_function, selection_function,
                                                              survival_function,
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

                                result = SimulationResult(size, problem, bullseye_fitness, mating_function, string_mutation,
                                                          selection_function, survival_function, mutation_rate, elite_rate,
                                                          iterations_performance, runtime_performance)
                                update_best(result, best_runtime, best_iterations)
                                add_results_to_sheet(stats, current_line, size, mating_function, selection_function, survival_function,
                                                     mutation_rate, elite_rate,
                                                     iterations_performance, runtime_performance, success_counter)
                                current_line += 1
    workbook.save('Simulation Report.xls')
    best_iterations.sort(key=lambda x: x.iterations_mean)
    best_runtime.sort(key=lambda x: x.runtime_mean)
    print("Best Iterations:")
    print_results(best_iterations)
    print("Best Runtime:")
    print_results(best_runtime)

    plot_results_list("Iterations", best_iterations)
    plot_results_list("Runtime", best_iterations)


def get_func_name(function):
    name = function.__name__
    name = name.replace('_', ' ')
    if name == "survival of the elite":
        name = "elitism"
    elif name == "survival of the young":
        name = "age-based"
    return name


if __name__ == '__main__':
    create_simulation_report()
    pass
