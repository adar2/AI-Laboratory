from random import uniform, randint, choice
from string import printable
from Constants import MUTATION_RATE


def string_mutation(chromosome):
    target_size = len(chromosome.data)
    index = randint(0, target_size - 1)
    new_char = list(choice(printable))
    chromosome.data = chromosome.data[:index] + new_char + chromosome.data[index + 1:]


def exchange_mutation(chromosome):
    target_size = len(chromosome.data)
    index1 = uniform(0, target_size - 1)
    index2 = uniform(0, target_size - 1)
    chromosome.data[index1], chromosome.data[index2] = chromosome.data[index2], chromosome.data[index1]


def displacement_mutation(chromosome):
    target_size = len(chromosome.data)
    start_index = uniform(0, target_size - 1)
    end_index = uniform(start_index, target_size - 1)
    displaced_items = chromosome.data[start_index:end_index + 1]
    del chromosome.data[start_index:end_index + 1]
    insertion_index = uniform(0, len(chromosome.data))
    chromosome.data = chromosome.data[:insertion_index] + displaced_items + chromosome.data[insertion_index + 1:]


def insertion_mutation(chromosome):
    target_size = len(chromosome.data)
    index_to_remove = randint(0, target_size - 1)
    item_to_insert = chromosome.data[index_to_remove]
    del chromosome.data[index_to_remove]
    chromosome.data.insert(uniform(0, len(chromosome.data)), item_to_insert)


def inversion_mutation(chromosome):
    target_size = len(chromosome.data)
    start_index = randint(0, target_size - 1)
    end_index = randint(start_index, target_size - 1)
    displaced_items = chromosome.data[start_index:end_index + 1]
    displaced_items.reverse()
    del chromosome.data[start_index:end_index + 1]
    insertion_index = randint(0, len(chromosome.data))
    chromosome.data = chromosome.data[:insertion_index] + displaced_items + chromosome.data[insertion_index + 1:]
