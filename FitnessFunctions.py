def absolute_distance_fitness(chromosome, target):
    chromosome.fitness = 0
    for i in range(len(target)):
        chromosome.fitness += abs(ord(chromosome.data[i]) - ord(target[i]))


def pso_distance_fitness(particle, target):
    particle.fitness = 0
    for i in range(len(target)):
        particle.fitness += abs(particle.position[i] - target[i])


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


def bullseye_fitness(chromosome, target):
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
