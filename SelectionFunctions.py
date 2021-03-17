from Constants import TRUNCATION_RATE

def get_fitness_proportional_distribution(population: list) -> list:


def truncation_selection(population: list):
    truncate_size = int(len(population) * TRUNCATION_RATE)
    return population[:truncate_size]
