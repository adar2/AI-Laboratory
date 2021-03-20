from random import randint, choice


def string_mutation(chromosome):
    target_size = len(chromosome.data)
    index = randint(0, target_size - 1)
    new_char = [choice(chromosome.problem.search_space)]
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
