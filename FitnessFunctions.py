import random


def absolute_distance_fitness(chromosome):
    chromosome.fitness = 0
    target = chromosome.problem.target
    for i in range(len(target)):
        chromosome.fitness += abs(ord(chromosome.search_space[i]) - ord(target[i]))


def pso_distance_fitness(particle, target):
    particle.fitness = 0
    for i in range(len(target)):
        particle.fitness += abs(particle.position[i] - target[i])


def n_queens_conflicts_fitness(chromosome):
    total_conflicts = 0
    game_board = chromosome.search_space
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
    while chromosome.problem.calc_capacity(chromosome.search_space) > capacity:
        rnd_index = random.randint(0, len(chromosome.search_space) - 1)
        chromosome.search_space[rnd_index] = 0
    chromosome.fitness = max_sum - chromosome.problem.calc_knapsack_value(chromosome.search_space)


def bullseye_fitness(chromosome):
    target = chromosome.problem.target
    chromosome.fitness = len(target) * 2
    BONUS_LEVEL_1 = 1
    BONUS_LEVEL_2 = 2

    target_hash = create_char_dict_from_collection(target)

    for i in range(len(chromosome.search_space)):
        current_char = chromosome.search_space[i]
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
