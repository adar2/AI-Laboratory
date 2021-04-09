from Problems.CVRP import CVRP
from Utils.CVRPFileParsing import parse_cvrp_file, getcwd

from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.LocalSearch.SimAnneal import SimAnneal

from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Algorithms.GeneticAlgorithm.FitnessFunctions import CVRP_fitness as fitness_func
from Algorithms.GeneticAlgorithm.MatingFunctions import ordered_crossover as mating_func
from Algorithms.GeneticAlgorithm.MutateFunctions import inversion_mutation as mutation_func
from Algorithms.GeneticAlgorithm.SelectionFunctions import deterministic_tournament_selection as selection_func
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite as survival_func


if __name__ == '__main__':
    files = ['\E-n22-k4.txt', '\E-n22-k5.txt', '\E-n33-k4.txt', '\E-n51-k5.txt', '\E-n76-k8.txt', '\E-n76-k10.txt', '\E-n101-k8.txt',
             '\E-n101-k14.txt']
    optimal_costs = [375,835,]
