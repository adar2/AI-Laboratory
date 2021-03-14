from random import randint, uniform, choice
import string


def mutate(chromosome, target_size):
    index = randint(0, target_size)
    new_char = choice(string.printable)
    chromosome.data[index] = new_char


def single_point_crossover(population, buffer, elite_size, target_size, mutation_rate):
    top_population = int(len(population) / 2)
    for i in range(elite_size, len(population)):
        index1 = randint(0, top_population)
        index2 = randint(0, top_population)
        crossover_index = randint(0, target_size)
        buffer[i].data = population[index1][:crossover_index] + population[index2][crossover_index]
        if uniform(0, 1) < mutation_rate:
            mutate(buffer[i], target_size)


def multi_point_crossover(population, buffer, elite_size, target_size, mutation_rate):
    top_population = int(len(population) / 2)
    for i in range(elite_size, len(population)):
        index1 = randint(0, top_population)
        index2 = randint(0, top_population)
        crossover_index_1 = randint(0, target_size)
        crossover_index_2 = randint(0, target_size)
        buffer[i].data = population[index1][:crossover_index_1] \
                         + population[index2][crossover_index_1, crossover_index_2] \
                         + population[index1][crossover_index_2]
        if uniform(0, 1) < mutation_rate:
            mutate(buffer[i], target_size)


def uniform_point_crossover(population, buffer, elite_size, target_size, mutation_rate):
    top_population = int(len(population) / 2)
    for i in range(elite_size, len(population)):
        index1 = randint(0, top_population)
        index2 = randint(0, top_population)
        for j in range(target_size):
            chosen_parent = choice([population[index1], population[index2]])
            buffer[i].data[j] = chosen_parent[j]
        if uniform(0, 1) < mutation_rate:
            mutate(buffer[i], target_size)