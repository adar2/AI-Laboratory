import json
import os.path

import Algorithms.GeneticAlgorithm.FitnessFunctions as FitnessFunctions
import Algorithms.GeneticAlgorithm.MatingFunctions as MatingFunctions
import Algorithms.GeneticAlgorithm.MutateFunctions as MutateFunctions
import Algorithms.GeneticAlgorithm.SelectionFunctions as SelectionFunctions
import Algorithms.GeneticAlgorithm.SurvivalFunctions as SurvivalFunctions
import Utils.Constants as Constants
from Algorithms.ACO.ACO import ACO
from Algorithms.CSPAlgorithms.BackJumpingAlgorithm import BackJumpingAlgorithm
from Algorithms.CSPAlgorithms.ForwardCheckingAlgorithm import ForwardCheckingAlgorithm
from Algorithms.GeneticAlgorithm.ColoringGeneticAlgorithm import ColoringGeneticAlgorithm
from Algorithms.GeneticAlgorithm.GeneralGeneticAlgorithm import GeneralGeneticAlgorithm
from Algorithms.LocalSearch.CVRPTabuSearch import CVRPTabuSearch
from Algorithms.LocalSearch.ColoringTabuSearch import ColoringTabuSearch
from Algorithms.LocalSearch.HybridColoringAlgorithm import HybridColoringAlgorithm
from Algorithms.LocalSearch.KempeChainsAlgorithm import KempeChainsAlgorithm
from Algorithms.LocalSearch.SimulatedAnnealing import SimulatedAnnealing
from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Algorithms.PSO.PSO import ParticleSwarmOptimization
from Problems.CVRP import CVRP
from Problems.GraphColoringProblem import GraphColoringProblem
from Problems.KnapSack import KnapSack
from Problems.NQueens import NQueens
from Problems.StringMatching import StringMatching
from Utils.CVRPFileParsing import parse_cvrp_file
from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing


def init_config():
    config = {
        "ALGORITHM": "GA",
        "POP_SIZE": "100",
        "MAX_ITER": "1000",
        "PROBLEM": "KNAPSACK",
        "TARGET": [165, [23, 31, 29, 44, 53, 38, 63, 85, 89, 82], [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]],
        "FITNESS_FUNC": "KNAPSACK_CLOSEST_FITNESS",
        "MATING_FUNC": "ORDERED_CROSSOVER",
        "MUTATION_FUNC": "STOCHASTIC_FLIP_MUTATION",
        "SELECTION_FUNC": "DETERMINISTIC_TOURNAMENT_SELECTION",
        "SURVIVAL_FUNC": "SURVIVAL_OF_THE_ELITE"
    }

    notes = ""
    notes += "// Available Algorithms:\n\n"
    algorithms = ['GA', 'PSO', 'ACO', 'TABU_SEARCH', 'SA', 'BACKJUMPING', 'FORWARD_CHECKING', 'KEMPE_CHAINS','HYBRID_COLORING']
    for a in algorithms:
        notes += f'// {a}\n\n'
    problems = ['STRING_MATCHING', 'NQUEENS', 'KNAPSACK', 'CVRP', 'GRAPH_COLORING']
    notes += "// Available Problems:\n\n"
    for p in problems:
        notes += f'// {p}\n\n'
    types = [(FitnessFunctions, 'fitness'), (MatingFunctions, 'crossover'), (MutateFunctions, 'mutation'),
             (SelectionFunctions, 'selection'), (SurvivalFunctions, 'survival')]
    for t in types:
        module_name = t[0]
        key_word = t[1]
        notes += f"// Available {module_name.__name__.split('.')[-1]}:\n\n"
        for c in dir(module_name):
            if key_word in c:
                notes += f"// {c.upper()}\n\n"
    with open('config.json', 'w') as f:
        json.dump(config, f)
        f.write('\n' + notes)


def get_config():
    if not os.path.isfile('config.json'):
        init_config()
    with open('config.json', 'r') as f:
        clean_json = ''.join(line for line in f if not line.startswith('//'))
        return json.loads(clean_json)


def get_algorithm(project_path):
    try:
        config = get_config()
        algorithm = config['ALGORITHM']
        pop_size = int(config['POP_SIZE'])
        max_iter = int(config['MAX_ITER'])
        problem = config['PROBLEM']
        target = config['TARGET']
        fitness_func = config['FITNESS_FUNC']
        fitness_func = getattr(FitnessFunctions, fitness_func.lower())
        mating_func = config['MATING_FUNC']
        mating_func = getattr(MatingFunctions, mating_func.lower())
        mutation_func = config['MUTATION_FUNC']
        mutation_func = getattr(MutateFunctions, mutation_func.lower())
        selection_func = config['SELECTION_FUNC']
        selection_func = getattr(SelectionFunctions, selection_func.lower())
        survival_func = config['SURVIVAL_FUNC']
        survival_func = getattr(SurvivalFunctions, survival_func.lower())
        if problem == 'STRING_MATCHING':
            problem = StringMatching(str(target))
        elif problem == 'NQUEENS':
            problem = NQueens(int(target))
        elif problem == 'KNAPSACK':
            capacity = target[0]
            weights = target[1]
            profits = target[2]
            problem = KnapSack(capacity, weights, profits)
        elif problem == 'CVRP':
            capacity, locations = parse_cvrp_file(project_path + '\\' + target)
            problem = CVRP(capacity, locations)
        elif problem == 'GRAPH_COLORING':
            graph, vertices, edges = coloring_problem_file_parsing(project_path + '\\' + target)
            problem = GraphColoringProblem(graph, vertices, edges)
        else:
            raise KeyError
        if algorithm == 'GA':
            if isinstance(problem, GraphColoringProblem):
                return ColoringGeneticAlgorithm(pop_size, max_iter, problem, fitness_func,
                                                mating_func, mutation_func)
            return GeneralGeneticAlgorithm(pop_size, max_iter, problem, fitness_func,
                                           mating_func, mutation_func, selection_func, survival_func)
        elif algorithm == 'PSO':
            return ParticleSwarmOptimization(pop_size, str(target), Constants.INERTIA_MIN, Constants.INERTIA_MAX,
                                             Constants.C1, Constants.C2, max_iter, fitness_func)
        elif algorithm == 'ACO':
            return ACO(problem, max_iter, pop_size)
        elif algorithm == 'TABU_SEARCH':
            if isinstance(problem, GraphColoringProblem):
                return ColoringTabuSearch(problem, max_iter)
            return CVRPTabuSearch(problem, max_iter)
        elif algorithm == 'SA':
            return SimulatedAnnealing(problem, max_iter)
        elif algorithm == 'BACKJUMPING':
            return BackJumpingAlgorithm(problem)
        elif algorithm == 'FORWARD_CHECKING':
            return ForwardCheckingAlgorithm(problem)
        elif algorithm == 'KEMPE_CHAINS':
            return KempeChainsAlgorithm(problem, max_iter)
        elif algorithm == 'HYBRID_COLORING':
            return HybridColoringAlgorithm(problem, max_iter)
        else:
            raise KeyError
    except KeyError as e:
        print("Unknown configuration")
        return None
