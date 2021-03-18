from Constants import OLD_AGE, FITNESS_CUTOFF_PCT, ELITE_RATE
from numpy import copy


def survival_of_the_good_and_young(population: list) -> list:
    survivors = []
    max_fitness = max(population)
    min_fitness_to_survive = FITNESS_CUTOFF_PCT * max_fitness
    for chromosome in population:
        if chromosome.age < OLD_AGE and chromosome.fitness > min_fitness_to_survive:
            survivors.append(chromosome)
    return survivors


def survival_of_the_elite(population: list) -> list:
    survivors = [copy(population)]
    survivors.sort(key=lambda x: x.fitness)
    chromosomes_to_keep = int(ELITE_RATE * len(population))
    return survivors[:chromosomes_to_keep]
