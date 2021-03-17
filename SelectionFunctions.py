from Constants import TRUNCATION_RATE
import numpy as np


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
