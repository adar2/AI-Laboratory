from Problems.CVRP import CVRP
from Utils.CVRPFileParsing import parse_cvrp_file, getcwd
from Algorithms.LocalSearch.TabuSearch import TabuSearch
# from Algorithms.LocalSearch.SimAnneal import SimAnneal

from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Algorithms.GeneticAlgorithm.FitnessFunctions import CVRP_fitness as fitness_func
from Algorithms.GeneticAlgorithm.MatingFunctions import ordered_crossover as mating_func
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation as mutation_func
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection as selection_func
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite as survival_func

import xlwt


def init_sheet(sheet):
    sheet.write(0, 0, "Algorithm")
    sheet.write(0, 1, "Problem")
    sheet.write(0, 2, "Found Solution")
    sheet.write(0, 3, "Found Solution Cost")
    sheet.write(0, 4, "Distance From Optimal")
    sheet.write(0, 5, "Run Time")


def add_ga_run():
    ga_algo = SimpleGeneticAlgorithm(pop_size, max_iter, cvrp_problem, fitness_func,
                                     mating_func, mutation_func, selection_func, survival_func)
    ga_algo.run()
    ga_sheet.write(line, 0, "GA")
    ga_sheet.write(line, 1, files[i])
    ga_sheet.write(line, 2, "True")
    ga_sheet.write(line, 3, ga_algo.best.fitness)
    ga_sheet.write(line, 4, abs(optimal_costs[i] - ga_algo.best.fitness))
    ga_sheet.write(line, 5, ga_algo.time_elapsed)



if __name__ == '__main__':
    # files = ['\E-n22-k4.txt','\E-n33-k4.txt', '\E-n51-k5.txt', '\E-n76-k8.txt', '\E-n76-k10.txt', '\E-n101-k8.txt',
    #          '\E-n101-k14.txt']
    # optimal_costs = [375,835,521,735,832,817,1077]
    workbook = xlwt.Workbook()
    files = ['\E-n22-k4.txt', '\E-n33-k4.txt']
    optimal_costs = [375, 835]

    # GA Simulations Setup
    ga_sheet = workbook.add_sheet('GA')
    init_sheet(ga_sheet)
    max_iter = 100
    pop_size = 50
    line = 1

    # TS Simulations Setup
    ts_sheet = workbook.add_sheet('TS')
    init_sheet(ts_sheet)

    # SA Simulations Setup
    sa_sheet = workbook.add_sheet('SA')
    init_sheet(sa_sheet)

    for i in range(len(files)):
        capacity, locations = parse_cvrp_file(getcwd() + files[i])
        cvrp_problem = CVRP(capacity, locations)
        for j in range(2):
            add_ga_run()
            line += 1
        workbook.save("CVRP_Simulation_GA.xls")







