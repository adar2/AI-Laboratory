import json
import os.path
from GeneticAlgorithm import SimpleGeneticAlgorithm
from PSO import ParticleSwarmOptimization
from StringMatching import StringMatching
from NQueens import NQueens
from KnapSack import KnapSack
import Constants


def init_config():
    config = {
        "ALGORITHM": "GA",
        "POP_SIZE": "2048",
        "MAX_ITER": "16368",
        "PROBLEM": "KNAPSACK",
        "TARGET": "[165, [23, 31, 29, 44, 53, 38, 63, 85, 89, 82], [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]]",
        "FITNESS_FUNC": "ABSOLUTE_DISTANCE_FITNESS",
        "MATING_FUNC": "ORDERED_CROSSOVER",
        "MUTATION_FUNC": "STRING_MUTATION",
        "SELECTION_FUNC": "DETERMINISTIC_TOURNAMENT_SELECTION",
        "SURVIVAL_FUNC": "SURVIVAL_OF_THE_ELITE",
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)


def get_config():
    if not os.path.isfile('config.json'):
        init_config()
    with open('config.json', 'r') as f:
        return json.load(f)


def get_algorithm():
    config = get_config()
    algorithm = config['ALGORITHM']
    pop_size = int(config['POP_SIZE'])
    max_iter = int(config['MAX_ITER'])
    problem = config['PROBLEM']
    target = config['TARGET']
    fitness_func = config['FITNESS_FUNC']
    fitness_func = getattr(__import__('FitnessFunctions'), fitness_func.lower())
    mating_func = config['MATING_FUNC']
    mating_func = getattr(__import__('MatingFunctions'), mating_func.lower())
    mutation_func = config['MUTATION_FUNC']
    mutation_func = getattr(__import__('MutateFunctions'), mutation_func.lower())
    selection_func = config['SELECTION_FUNC']
    selection_func = getattr(__import__('SelectionFunctions'), selection_func.lower())
    survival_func = config['SURVIVAL_FUNC']
    survival_func = getattr(__import__('SurvivalFunctions'), survival_func.lower())
    if problem == 'STRING_MATCHING':
        problem = StringMatching(str(target))
    elif problem == 'NQueens':
        problem = NQueens(int(target))
    elif problem == 'KNAPSACK':
        capacity = target[0]
        weights = target[1]
        profits = target[2]
        problem = KnapSack(capacity, weights, profits)
    if algorithm == 'GA':
        return SimpleGeneticAlgorithm(pop_size, max_iter, problem, fitness_func,
                                      mating_func, mutation_func, selection_func, survival_func)
    elif algorithm == 'PSO':
        return ParticleSwarmOptimization(pop_size, str(target), Constants.INERTIA_MIN, Constants.INERTIA_MAX,
                                         Constants.C1, Constants.C2, max_iter, fitness_func)
