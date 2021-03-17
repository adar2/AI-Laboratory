from random import randint, choice
from Chromosome import Chromosome


def single_point_crossover(parent_1: Chromosome, parent_2: Chromosome):
    target_size = len(parent_1.data)
    crossover_index = randint(0, target_size)
    new_data = parent_1.data[:crossover_index] + parent_2.data[crossover_index:]
    return Chromosome(new_data)


# for i in range(survivor_rate, len(population)):
#     index1 = randint(0, top_population)
#     index2 = randint(0, top_population)
#     buffer[i].data = population[index1].data[:crossover_index] + population[index2].data[crossover_index:]
#     mutate(buffer[i], target_size)


def multi_point_crossover(parent_1: Chromosome, parent_2: Chromosome):
    target_size = len(parent_1.data)
    crossover_index_1 = randint(0, target_size - 1)
    crossover_index_2 = randint(crossover_index_1, target_size - 1)
    new_data = parent_1.data[:crossover_index_1] \
               + parent_2.data[crossover_index_1:crossover_index_2] \
               + parent_1.data[crossover_index_2:]
    return Chromosome(new_data)


def uniform_point_crossover(parent_1: Chromosome, parent_2: Chromosome):
    target_size = len(parent_1.data)
    child = Chromosome(parent_1.data)
    for j in range(target_size):
        chosen_parent = choice([parent_1, parent_2])
        child.data = child.data[:j] + chosen_parent.data[j] + child.data[j + 1:]
    return child
