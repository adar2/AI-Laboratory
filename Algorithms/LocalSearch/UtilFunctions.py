from math import sqrt
from Problems.CVRP import CVRP
from Problems.GraphColoringProblem import GraphColoringProblem
from Utils.Constants import COORDINATES


def CVRP_init_config(problem: CVRP):
    config = []
    search_space = problem.get_search_space()
    current_location = search_space[0]
    search_space = search_space[1:]
    config.append(current_location)
    while search_space:
        min_location = None
        min_location_distance = 0
        for location in search_space:
            distance = euc_distance(current_location[COORDINATES], location[COORDINATES])
            if min_location is None or distance < min_location_distance:
                min_location = location
                min_location_distance = distance
        current_location = min_location
        config.append(current_location)
        search_space.remove(current_location)
    return config


def coloring_init_config(problem: GraphColoringProblem):
    graph = problem.get_search_space()
    vertices_color_dict = {}
    current_max_color = 1
    colors_domain = [1]
    for vertex in graph:
        neighbors_colors = [vertices_color_dict[neighbor] for neighbor in graph[vertex] if
                            neighbor in vertices_color_dict]
        available_colors = [color for color in colors_domain if color not in neighbors_colors]
        # if available colors list is empty increase maximum color by 1 and assign it to vertex
        if not available_colors:
            current_max_color += 1
            colors_domain.append(current_max_color)
            vertices_color_dict[vertex] = current_max_color
            continue
        # if the available colors list is not empty assign to vertex the first color in that list
        vertices_color_dict[vertex] = available_colors[0]
    return [vertex_color for vertex_color in vertices_color_dict.values()]


def euc_distance(cords_a: tuple, cords_b: tuple):
    X, Y = 0, 1
    return sqrt((cords_a[X] - cords_b[X]) ** 2 + (cords_a[Y] - cords_b[Y]) ** 2)


def cvrp_path_cost(problem: CVRP, config):
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


def coloring_cost(problem:GraphColoringProblem,config:list):
    bad_edges = []
    graph = problem.get_search_space()
    for vertex in range(len(config)):
        for constraint_vertex in graph[vertex + 1]:
            # avoid adding the bad edge from both sides
            if config[vertex] == config[constraint_vertex - 1] and (constraint_vertex - 1, vertex) not in bad_edges:
                bad_edges.append((vertex, constraint_vertex - 1))
    return len(bad_edges)