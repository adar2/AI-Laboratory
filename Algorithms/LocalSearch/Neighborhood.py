import copy
from random import choice, randint
from copy import deepcopy
from math import sqrt


def __relocate(solution: list, customer: tuple) -> list:
    customer_index = solution.index(customer)
    results = []
    for i in range(len(solution)):
        if i == customer_index:
            continue
        temp_solution = deepcopy(solution)
        temp_solution.remove(customer)
        temp_solution = temp_solution[:i] + [customer] + temp_solution[i:]
        # temp_solution.insert(i, customer)
        # if i < customer_index:
        #     del temp_solution[customer_index + 1]
        # else:
        #     del temp_solution[customer_index - 1]
        results.append(temp_solution)
    return results


def __switch(solution: list, index_1: int, index_2: int) -> any:
    solution[index_1], solution[index_2] = solution[index_2], solution[index_1]


def __exchange(solution: list, customer: tuple) -> list:
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
    moves = [__relocate, __exchange]
    for i in range(3):
        selected_move = choice(moves)
        for item in selected_move(solution, customer):
            neighborhood.append(item)
        customer = choice(solution)
    return neighborhood


def __get_valid_colors(vertex, config, graph, coloring):
    neighbors_colors = [config[neighbor - 1] for neighbor in graph[vertex + 1]]
    return [color for color in list(range(1, coloring + 1)) if color not in neighbors_colors]





