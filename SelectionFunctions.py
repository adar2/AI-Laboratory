from Constants import TRUNCATION_RATE, PCT_OF_PARENT, TOURNAMENT_PARTICIPANTS
from math import sqrt
import numpy as np
import random


def get_fitness_proportional_distribution(population: list) -> list:
    # scaling done by applying sqrt function on the chromosomes fitness value
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
    population.sort(key=lambda x: x.fitness)
    truncate_size = int(len(population) * TRUNCATION_RATE)
    return population[:truncate_size]


def rws(population: list) -> list:
    selected = []
    fpd = get_fitness_proportional_distribution(population)
    offspring = int(len(population)*PCT_OF_PARENT)
    for i in range(offspring):
        r = random.random()
        i = 0
        while fpd[i] < r:
            i += 1
        selected.append(population[i])
    return selected


def sus(population: list) -> list:
    selected = []
    population_size = len(population)
    offspring = int(population_size * PCT_OF_PARENT)
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


def deterministic_tournament_selection(population: list) -> list:
    selected = []
    offspring = int(len(population) * PCT_OF_PARENT)
    participants = int(TOURNAMENT_PARTICIPANTS * len(population))
    for i in range(offspring):
        sample = random.sample(population, participants)
        sample.sort(key=lambda x: x.fitness)
        selected.append(sample[0])
    return selected


def stochastic_tournament_selection(population: list) -> list:
    selected = []
    offspring = int(len(population) * PCT_OF_PARENT)
    participants = int(TOURNAMENT_PARTICIPANTS * len(population))
    for i in range(offspring):
        sample = random.sample(population, participants)
        fpd = get_fitness_proportional_distribution(sample)
        selected.append(random.choices(sample, fpd)[0])
    return selected
