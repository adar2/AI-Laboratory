from Constants import TRUNCATION_RATE


def truncation_selection(population: list):
    truncate_size = len(population) * TRUNCATION_RATE
    return population[:truncate_size]
