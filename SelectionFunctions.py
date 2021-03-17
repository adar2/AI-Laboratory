from Constants import TRUNCATION_RATE
import numpy as np
import random


def get_fitness_proportional_distribution(population: list) -> list:
    result = []
    fitness_sum = 0
    for chromosome in population:
        fitness_sum += chromosome.fitness
    for chromosome in population:
        probability = chromosome.fitness / fitness_sum
        result.append(probability)
    result.reverse()
    result = list(np.cumsum(result))
    return result


def truncation_selection(population: list) -> list:
    truncate_size = int(len(population) * TRUNCATION_RATE)
    return population[:truncate_size]


def rws(population: list, offspring: int) -> list:
    selected = []
    fpd = get_fitness_proportional_distribution(population)
    for i in range(offspring):
        r = random.random()
        i = 0
        while fpd[i] < r:
            i += 1
        selected.append(population[i])
    return selected


def sus(population: list, offspring: int) -> list:
    selected = []
    population_size = len(population)
    fpd = get_fitness_proportional_distribution(population)
    step = 1 / offspring
    start = random.uniform(0, step)
    points = [start + i * step for i in range(offspring)]
    for point in points:
        i = 0
        while fpd[i] < point:
            i += 1
            if i >= population_size:
                i = 0
        selected.append(population[i])
    return selected


def tournament_selection(population: list, k: int, offspring: int) -> list:
    selected = []
    for i in range(offspring):
        sample = random.sample(population, k)
        sample.sort(key=lambda x: x.fitness)
        selected.append(sample[0])
    return selected
