import json
import os.path
from Algorithms.GeneticAlgorithm.GeneticAlgorithm import SimpleGeneticAlgorithm
from Algorithms.PSO.PSO import ParticleSwarmOptimization
from Problems.StringMatching import StringMatching
from Problems.NQueens import NQueens
from Problems.KnapSack import KnapSack
import Constants


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
    notes += "// Available Algorithms:\n"
    algorithms = ['GA', 'PSO']
    for a in algorithms:
        notes += f'// {a}\n'
    problems = ['STRING_MATCHING', 'NQUEENS', 'KNAPSACK']
    notes += "// Available Problems:\n"
    for p in problems:
        notes += f'// {p}\n'
    types = [('FitnessFunctions', 'fitness'), ('MatingFunctions', 'crossover'), ('MutateFunctions', 'mutation'),
             ('SelectionFunctions', 'selection'), ('SurvivalFunctions', 'survival')]
    for t in types:
        module_name = t[0]
        key_word = t[1]
        notes += f"// Available {module_name}:\n"
        for c in dir(__import__(module_name)):
            if key_word in c:
                notes += f"// {c.upper()}\n"
    with open('config.json', 'w') as f:
        json.dump(config, f)
        f.write('\n' + notes)


def get_config():
    if not os.path.isfile('config.json'):
        init_config()
    with open('config.json', 'r') as f:
        clean_json = ''.join(line for line in f if not line.startswith('//'))
        return json.loads(clean_json)


def get_algorithm():
    try:
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
        elif problem == 'NQUEENS':
            problem = NQueens(int(target))
        elif problem == 'KNAPSACK':
            capacity = target[0]
            weights = target[1]
            profits = target[2]
            problem = KnapSack(capacity, weights, profits)
        else:
            raise KeyError
        if algorithm == 'GA':
            return SimpleGeneticAlgorithm(pop_size, max_iter, problem, fitness_func,
                                          mating_func, mutation_func, selection_func, survival_func)
        elif algorithm == 'PSO':
            return ParticleSwarmOptimization(pop_size, str(target), Constants.INERTIA_MIN, Constants.INERTIA_MAX,
                                             Constants.C1, Constants.C2, max_iter, fitness_func)
        else:
            raise KeyError
    except KeyError as e:
        print("Unknown configuration")
        return None
