from random import choice
from copy import deepcopy


def __relocate(solution: list, customer: tuple) -> list:
    customer_index = solution.index(customer)
    results = []
    for i in range(len(solution)):
        temp_solution = deepcopy(solution)
        if i == customer_index:
            continue
        temp_solution.insert(i, customer)
        if i < customer_index:
            del temp_solution[customer_index + 1]
        else:
            del temp_solution[customer_index - 1]
        results.append(temp_solution)
    return results


def __switch(solution: list, index_1: int, index_2: int) -> any:
    solution[index_1], solution[index_2] = solution[index_2], solution[index_1]


def __exchange(solution: list, customer : tuple) -> list:
    results = []
    customer_index = solution.index(customer)
    for i in range(len(solution)):
        temp_solution = deepcopy(solution)
        if i != customer_index:
            __switch(temp_solution, i, customer_index)
            results.append(temp_solution)
    return results


def random_move_neighborhood(solution: list) -> list:
    neighborhood = []
    customer = choice(solution)
    for i in range(3):
        moves = [__relocate, __exchange]
        selected_move = choice(moves)
        for item in selected_move(solution, customer):
            neighborhood.append(item)
        new_customer = choice(solution)
        while new_customer == customer:
            new_customer = choice(solution)
    return neighborhood
