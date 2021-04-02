import random
from math import sqrt
from Chromosome import Chromosome


def __euc_distance(cords_a: tuple, cords_b: tuple):
    X, Y = 0, 1
    return sqrt((cords_a[X] - cords_b[X]) ** 2 + (cords_a[Y] - cords_b[Y]) ** 2)


def absolute_distance_fitness(chromosome):
    chromosome.fitness = 0
    target = chromosome.problem.target
    for i in range(len(target)):
        chromosome.fitness += abs(ord(chromosome.data[i]) - ord(target[i]))


def pso_distance_fitness(particle, target):
    particle.fitness = 0
    for i in range(len(target)):
        particle.fitness += abs(particle.position[i] - target[i])


def CVRP_fitness(chromosome: Chromosome):
    trucks = chromosome.problem.generate_truck_partition(chromosome.data)
    storage = chromosome.problem.get_search_space()[0]
    sum = 0
    COORDINATES = 0
    for truck in trucks:
        sum += __euc_distance(storage[COORDINATES], truck[0][COORDINATES])
        for i in range(len(truck) - 1):
            sum += __euc_distance(truck[i][COORDINATES], truck[i + 1][COORDINATES])
        sum += __euc_distance(truck[-1][COORDINATES], storage[COORDINATES])
    chromosome.fitness = sum


def n_queens_conflicts_fitness(chromosome):
    total_conflicts = 0
    game_board = chromosome.data
    for i in game_board:
        for j in game_board:
            if i == j:
                continue
            if abs(j - i) == abs(game_board.index(j) - game_board.index(i)):
                total_conflicts += 1
    chromosome.fitness = total_conflicts


def knapsack_closest_fitness(chromosome):
    capacity = chromosome.problem.get_capacity()
    max_sum = chromosome.problem.get_max_value()
    while chromosome.problem.calc_capacity(chromosome.data) > capacity:
        rnd_index = random.randint(0, len(chromosome.data) - 1)
        chromosome.data[rnd_index] = 0
    chromosome.fitness = max_sum - chromosome.problem.calc_knapsack_value(chromosome.data)


def bullseye_fitness(chromosome):
    target = chromosome.problem.target
    chromosome.fitness = len(target) * 2
    BONUS_LEVEL_1 = 1
    BONUS_LEVEL_2 = 2

    target_hash = create_char_dict_from_collection(target)

    for i in range(len(chromosome.data)):
        current_char = chromosome.data[i]
        if current_char in target_hash.keys():
            if target[i] == current_char:
                chromosome.fitness -= BONUS_LEVEL_2
                if target_hash[current_char] is False:
                    target_hash[current_char] = True
            elif target_hash[current_char] is False:
                target_hash[current_char] = True
                chromosome.fitness -= BONUS_LEVEL_1


def create_char_dict_from_collection(collection):
    result = {}
    for char in collection:
        result[char] = False
    return result
