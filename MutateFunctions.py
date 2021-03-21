from random import randint, choice, random


def string_mutation(chromosome):
    target_size = len(chromosome.search_space)
    index = randint(0, target_size - 1)
    new_char = [choice(chromosome.problem.search_space)]
    chromosome.search_space = chromosome.search_space[:index] + new_char + chromosome.search_space[index + 1:]


def exchange_mutation(chromosome):
    target_size = len(chromosome.search_space)
    index1 = randint(0, target_size - 1)
    index2 = randint(0, target_size - 1)
    chromosome.search_space[index1], chromosome.search_space[index2] = chromosome.search_space[index2], chromosome.search_space[index1]


def flip_mutation(chromosome):
    rnd_index = randint(0, len(chromosome.search_space) - 1)
    if chromosome.search_space[rnd_index]:
        chromosome.search_space[rnd_index] = 0
    else:
        chromosome.search_space[rnd_index] = 1


def stochastic_flip_mutation(chromosome):
    for i in range(len(chromosome.search_space)):
        if random() <= 0.1:
            if chromosome.search_space[i]:
                chromosome.search_space[i] = 0
            else:
                chromosome.search_space[i] = 1


def displacement_mutation(chromosome):
    target_size = len(chromosome.search_space)
    start_index = randint(0, target_size - 1)
    end_index = randint(start_index, target_size - 1)
    displaced_items = chromosome.search_space[start_index:end_index + 1]
    if len(displaced_items) == target_size:
        return
    del chromosome.search_space[start_index:end_index + 1]
    insertion_index = randint(0, len(chromosome.search_space) - 1)
    chromosome.search_space = chromosome.search_space[:insertion_index] + displaced_items + chromosome.search_space[insertion_index:]


def insertion_mutation(chromosome):
    target_size = len(chromosome.search_space)
    index_to_remove = randint(0, target_size - 1)
    item_to_insert = chromosome.search_space[index_to_remove]
    del chromosome.search_space[index_to_remove]
    chromosome.search_space.insert(randint(0, len(chromosome.search_space)), item_to_insert)


def inversion_mutation(chromosome):
    target_size = len(chromosome.search_space)
    start_index = randint(0, target_size - 1)
    end_index = randint(start_index, target_size - 1)
    displaced_items = chromosome.search_space[start_index:end_index + 1]
    displaced_items.reverse()
    del chromosome.search_space[start_index:end_index + 1]
    insertion_index = randint(0, len(chromosome.search_space))
    chromosome.search_space = chromosome.search_space[:insertion_index] + displaced_items + chromosome.search_space[insertion_index:]
