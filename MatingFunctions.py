from random import randint, choice, uniform
from copy import deepcopy
from Chromosome import Chromosome


def single_point_crossover(parent_1: Chromosome, parent_2: Chromosome):
    target_size = len(parent_1.data)
    crossover_index = randint(0, target_size)
    new_data = parent_1.data[:crossover_index] + parent_2.data[crossover_index:]
    return Chromosome(parent_1.problem, new_data)


def multi_point_crossover(parent_1: Chromosome, parent_2: Chromosome):
    target_size = len(parent_1.data)
    crossover_index_1 = randint(0, target_size - 1)
    crossover_index_2 = randint(crossover_index_1, target_size - 1)
    new_data = parent_1.data[:crossover_index_1] \
               + parent_2.data[crossover_index_1:crossover_index_2] \
               + parent_1.data[crossover_index_2:]
    return Chromosome(parent_1.problem, new_data)


def uniform_point_crossover(parent_1: Chromosome, parent_2: Chromosome):
    target_size = len(parent_1.data)
    child = Chromosome(parent_1.problem, parent_1.data)
    for j in range(target_size):
        chosen_parent = choice([parent_1, parent_2])
        child.data = child.data[:j] + [chosen_parent.data[j]] + child.data[j + 1:]
    return child


def ordered_crossover(parent_1: Chromosome, parent_2: Chromosome):
    target_size = len(parent_1.data)
    parent_2_clone = deepcopy(parent_2)
    child_data = [None] * target_size
    start_index = randint(0, target_size - 1)
    end_index = randint(start_index, target_size - 1)
    for i in range(start_index, end_index + 1):
        child_data[i] = parent_1.data[i]
    for item in range(len(child_data)):
        if item in child_data:
            parent_2_clone.data.remove(item)
    for i in range(len(child_data)):
        if child_data[i] is None:
            child_data[i] = parent_2_clone.data[0]
            del parent_2_clone.data[0]
    return Chromosome(parent_1.problem, child_data)


def partially_matched_crossover(parent_1: Chromosome, parent_2: Chromosome):
    target_size = len(parent_1.data)
    index = randint(0, target_size - 1)
    num_1 = parent_1.data[index]
    num_2 = parent_2.data[index]
    offspring_1_data, offspring_2_data = __generate_offsprings(num_1, num_2, parent_1, parent_2)
    return Chromosome(parent_1.problem, choice([offspring_1_data, offspring_2_data]))


def __generate_offsprings(num_1, num_2, parent_1, parent_2):
    parent_1_num_1_index = parent_1.search_space.index(num_1)
    parent_1_num_2_index = parent_1.search_space.index(num_2)
    parent_2_num_1_index = parent_1.search_space.index(num_1)
    parent_2_num_2_index = parent_1.search_space.index(num_2)
    offspring_1_data = deepcopy(parent_1.search_space)
    offspring_1_data[parent_1_num_1_index], offspring_1_data[parent_1_num_2_index] = offspring_1_data[
                                                                                         parent_1_num_2_index], \
                                                                                     offspring_1_data[
                                                                                         parent_1_num_1_index]
    offspring_2_data = deepcopy(parent_2.search_space)
    offspring_2_data[parent_2_num_1_index], offspring_2_data[parent_2_num_2_index] = offspring_2_data[
                                                                                         parent_2_num_2_index], \
                                                                                     offspring_2_data[
                                                                                         parent_2_num_1_index]
    return offspring_1_data, offspring_2_data
