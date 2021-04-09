# String Matching
# Parameters:
# - Population Size
# - Mutation Rate
# - Elite Rate
# - Selection Function
# - Survival Function
# - Mating Function
# - Mutation Function
from GASimulationResult import GASimulationResult
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite, survival_of_the_young
from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation, exchange_mutation, insertion_mutation, displacement_mutation
from Algorithms.GeneticAlgorithm.MatingFunctions import ordered_crossover, \
    partially_matched_crossover
from Problems.NQueens import NQueens
from Algorithms.GeneticAlgorithm.FitnessFunctions import n_queens_conflicts_fitness
from Algorithms.GeneticAlgorithm import SelectionFunctions
from matplotlib import pyplot as plt
from statistics import mean
from Algorithms.MinConflicts.MinConflictAlgorithm import MinConflictAlgorithm
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
    if len(iterations_performance) > 0:
        stats.write(line, 8, round(mean(iterations_performance), 2))
    if len(runtime_performance) > 0:
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


def compare_nqueens_GA_minconflicts():
    nqueens_for_ga = NQueens(8)
    runs = range(100)
    ga_1_runtimes = []
    ga_2_runtimes = []
    minconf_runtimes = []
    ga_1_sucess_counter = 0
    ga_2_sucess_counter = 0
    minconf_sucess_counter = 0
    for run in runs:
        ga_1 = SimpleGeneticAlgorithm(256, 200, nqueens_for_ga, n_queens_conflicts_fitness, ordered_crossover, displacement_mutation,
                                      SelectionFunctions.stochastic_tournament_selection, survival_of_the_elite, 0.25, 0.6)
        ga_2 = SimpleGeneticAlgorithm(256, 200, nqueens_for_ga, n_queens_conflicts_fitness, ordered_crossover, displacement_mutation,
                                      SelectionFunctions.stochastic_tournament_selection, survival_of_the_elite, 0.25, 0.8)
        ga_1.run()
        ga_2.run()
        minconf = MinConflictAlgorithm(8, 200)
        minconf.run()
        if ga_1.solved:
            ga_1_sucess_counter += 1
        ga_1_runtimes.append(ga_1.time_elapsed)
        if ga_2.solved:
            ga_2_sucess_counter += 1
        ga_2_runtimes.append(ga_2.time_elapsed)
        minconf_runtimes.append(minconf.time_elapsed)
        if minconf.solved:
            minconf_sucess_counter += 1
    print(f'GA1 solved {ga_1_sucess_counter}, GA2 solved {ga_2_sucess_counter}, MinConf solved {minconf_sucess_counter}')
    plt.plot(runs, ga_1_runtimes)
    plt.plot(runs, ga_2_runtimes)
    plt.plot(runs, minconf_runtimes)
    plt.legend(['Configuration 1', 'Configuration 2', 'Min Conflicts'])
    plt.title("Comparison between GA and Min Conflicts (8-Queens)")
    plt.xlabel("Runs")
    plt.ylabel("Runtime in sec")
    plt.show()

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = ['Config 1', 'Config 2', 'Min Conflicts']
    success = [ga_1_sucess_counter, ga_2_sucess_counter, minconf_sucess_counter]
    plt.bar(langs, success)
    plt.xlabel('Algorithms')
    plt.ylabel('Number Of Successes')
    plt.title('Successes out of 100 runs')
    plt.show()




def create_simulation_report():
    # prepare run parameters
    # ** complete parameters for N-Queens**
    pop_sizes = [256, 512, 1024]
    mutation_rates = [0.25, 0.5, 0.75]
    selection_functions = [SelectionFunctions.truncation_selection, SelectionFunctions.stochastic_tournament_selection,
                           SelectionFunctions.roulette_wheel_selection, SelectionFunctions.stochastic_universal_sampling_selection]
    mating_functions = [ordered_crossover, partially_matched_crossover]
    mutation_functions = [exchange_mutation, insertion_mutation, inversion_mutation, displacement_mutation]
    survival_functions = [survival_of_the_elite, survival_of_the_young]
    elite_rates = [0.6, 0.8, 0.9]
    problem = NQueens(8)

    # pop_sizes = [1024]
    # mutation_rates = [0.25, 0.5, 0.75]
    # selection_functions = [SelectionFunctions.truncation_selection]
    # mating_functions = [ordered_crossover, partially_matched_crossover]
    # mutation_functions = [exchange_mutation, insertion_mutation, inversion_mutation, displacement_mutation]
    # survival_functions = [survival_of_the_elite]
    # elite_rates = [0.6, 0.8]
    # problem = NQueens(8)

    # prepare excel workbook
    workbook = xlwt.Workbook()
    stats = workbook.add_sheet('NQueens_Stats_1')
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
                                algo = SimpleGeneticAlgorithm(size, 5000, problem, n_queens_conflicts_fitness,
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

                                result = GASimulationResult(size, problem, n_queens_conflicts_fitness, mating_function,
                                                            mutation_function,
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
    compare_nqueens_GA_minconflicts()
    pass
