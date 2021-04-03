from Problems.AbstractProblem import AbstractProblem
from math import sqrt


def euc_distance(cords_a: tuple, cords_b: tuple):
    X, Y = 0, 1
    return sqrt((cords_a[X] - cords_b[X]) ** 2 + (cords_a[Y] - cords_b[Y]) ** 2)


def cvrp_path_cost(problem: AbstractProblem, config):
    trucks = problem.generate_truck_partition(config)
    storage = problem.get_search_space()[0]
    sum = 0
    COORDINATES = 0
    for truck in trucks:
        sum += euc_distance(storage[COORDINATES], truck[0][COORDINATES])
        for i in range(len(truck) - 1):
            sum += euc_distance(truck[i][COORDINATES], truck[i + 1][COORDINATES])
        sum += euc_distance(truck[-1][COORDINATES], storage[COORDINATES])
    return int(sum)
