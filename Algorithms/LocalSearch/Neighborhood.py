from copy import deepcopy, copy
from random import choice, randint
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


def random_vertex_neighborhood(graph: dict, config: list, coloring: int) -> list:
    neighborhood = []
    number_of_vertices = randint(2, int(sqrt(len(config))))
    vertex_list = []
    for i in range(number_of_vertices):
        vertex = randint(0, len(config) - 1)
        while vertex in vertex_list:
            vertex = randint(0, len(config) - 1)
        vertex_list.append(vertex)
    for vertex in vertex_list:
        valid_colors = __get_valid_colors(vertex, config, graph, coloring)
        for color in valid_colors:
            new_config = copy(config)
            new_config[vertex] = color
            neighborhood.append(new_config)
    return neighborhood
