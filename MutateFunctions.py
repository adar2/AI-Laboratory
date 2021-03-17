from random import uniform, randint, choice
from string import printable
from Constants import MUTATION_RATE


def string_mutation(chromosome):
    target_size = len(chromosome.data)
    index = randint(0, target_size - 1)
    new_char = choice(printable)
    chromosome.data = chromosome.data[:index] + new_char + chromosome.data[index + 1:]

