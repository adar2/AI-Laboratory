from Constants import OLD_AGE, ELITE_RATE
from numpy import copy


def survival_of_the_young(population: list) -> list:
    survivors = []
    for chromosome in population:
        if chromosome.age < OLD_AGE:
            survivors.append(chromosome)
    return survivors


def survival_of_the_elite(population: list, elite_rate: float) -> list:
    survivors = list(copy(population))
    survivors.sort(key=lambda x: x.fitness)
    chromosomes_to_keep = int(elite_rate * len(population))
    return survivors[:chromosomes_to_keep]
