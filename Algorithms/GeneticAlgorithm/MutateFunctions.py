from random import randint, choice, random
from Chromosome import Chromosome


def __is_in_conflict(vertex: int, bad_edges_list: list):
    for edge in bad_edges_list:
        if edge[0] == vertex:
            return True
    return False


def __generate_adjacent_colors(chromosome, vertex):
    colors = []
    graph = chromosome.problem.get_search_space()
    chromosome_coloring = chromosome.data
    adjacent_vertices = graph[vertex]
    for adjacent_vertex in adjacent_vertices:
        # the color of every vertex can be found in the current coloring under index: vertex_number-1
        colors.append(chromosome_coloring[adjacent_vertex-1])
    return colors


def coloring_mutation(chromosome:Chromosome, coloring:int, bad_edges_list: list):
    for i in range(len(chromosome.data)):
        vertex = chromosome.data[i]
        if __is_in_conflict(vertex, bad_edges_list):
            all_colors = list(range(1,coloring))
            adjacent_colors = __generate_adjacent_colors(chromosome, vertex)
            valid_colors = [color for color in all_colors if color not in adjacent_colors]
            if len(valid_colors) == 0:
                chromosome.data[i] = choice(all_colors)
            else:
                chromosome.data[i] = choice(valid_colors)





def string_mutation(chromosome):
    target_size = len(chromosome.data)
    index = randint(0, target_size - 1)
    new_char = [choice(chromosome.cvrp_problem.search_space)]
    chromosome.data = chromosome.data[:index] + new_char + chromosome.data[index + 1:]


def exchange_mutation(chromosome):
    target_size = len(chromosome.data)
    index1 = randint(0, target_size - 1)
    index2 = randint(0, target_size - 1)
    chromosome.data[index1], chromosome.data[index2] = chromosome.data[index2], chromosome.data[index1]


def flip_mutation(chromosome):
    rnd_index = randint(0, len(chromosome.data) - 1)
    if chromosome.data[rnd_index]:
        chromosome.data[rnd_index] = 0
    else:
        chromosome.data[rnd_index] = 1


def stochastic_flip_mutation(chromosome):
    for i in range(len(chromosome.data)):
        if random() <= 0.1:
            if chromosome.data[i]:
                chromosome.data[i] = 0
            else:
                chromosome.data[i] = 1


def displacement_mutation(chromosome):
    target_size = len(chromosome.data)
    start_index = randint(0, target_size - 1)
    end_index = randint(start_index, target_size - 1)
    displaced_items = chromosome.data[start_index:end_index + 1]
    if len(displaced_items) == target_size:
        return
    del chromosome.data[start_index:end_index + 1]
    insertion_index = randint(0, len(chromosome.data) - 1)
    chromosome.data = chromosome.data[:insertion_index] + displaced_items + chromosome.data[insertion_index:]


def insertion_mutation(chromosome):
    target_size = len(chromosome.data)
    index_to_remove = randint(0, target_size - 1)
    item_to_insert = chromosome.data[index_to_remove]
    del chromosome.data[index_to_remove]
    chromosome.data.insert(randint(0, len(chromosome.data)), item_to_insert)


def inversion_mutation(chromosome):
    target_size = len(chromosome.data)
    start_index = randint(0, target_size - 1)
    end_index = randint(start_index, target_size - 1)
    displaced_items = chromosome.data[start_index:end_index + 1]
    displaced_items.reverse()
    del chromosome.data[start_index:end_index + 1]
    insertion_index = randint(0, len(chromosome.data))
    chromosome.data = chromosome.data[:insertion_index] + displaced_items + chromosome.data[insertion_index:]
