import string
from random import randint, uniform, choice


def mutate(chromosome, target_size, mutation_rate):
    if uniform(0, 1) < mutation_rate:
        index = randint(0, target_size - 1)
        new_char = choice(string.printable)
        chromosome.data = chromosome.data[:index] + new_char + chromosome.data[index + 1:]


def single_point_crossover(population, buffer, elite_size, target_size, mutation_rate):
    top_population = int(len(population) / 2)
    for i in range(elite_size, len(population)):
        index1 = randint(0, top_population)
        index2 = randint(0, top_population)
        crossover_index = randint(0, target_size)
        buffer[i].data = population[index1].data[:crossover_index] + population[index2].data[crossover_index:]
        mutate(buffer[i], target_size, mutation_rate)


def multi_point_crossover(population, buffer, elite_size, target_size, mutation_rate):
    top_population = int(len(population) / 2)
    for i in range(elite_size, len(population)):
        index1 = randint(0, top_population)
        index2 = randint(0, top_population)
        crossover_index_1 = randint(0, target_size-1)
        crossover_index_2 = randint(crossover_index_1, target_size-1)
        buffer[i].data = population[index1].data[:crossover_index_1] \
                         + population[index2].data[crossover_index_1:crossover_index_2] \
                         + population[index1].data[crossover_index_2:]
        mutate(buffer[i], target_size, mutation_rate)


def uniform_point_crossover(population, buffer, elite_size, target_size, mutation_rate):
    top_population = int(len(population) / 2)
    for i in range(elite_size, len(population)):
        index1 = randint(0, top_population)
        index2 = randint(0, top_population)
        for j in range(target_size):
            chosen_parent = choice([population[index1], population[index2]])
            buffer[i].data = buffer[i].data[:j] + chosen_parent.data[j] + buffer[i].data[j+1:]

        mutate(buffer[i], target_size, mutation_rate)
