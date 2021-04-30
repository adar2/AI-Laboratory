from copy import copy


def minimum_remaining_values(vertices_color_dict: dict, legal_values_dict: dict, vertices_degree: dict):
    legal_values_dict_copy = copy(legal_values_dict)
    for key in vertices_color_dict.keys():
        legal_values_dict_copy.pop(key)
    if len(legal_values_dict_copy) == 0:
        return None
    min_value_index = min(legal_values_dict_copy.keys(), key=lambda key: len(legal_values_dict_copy[key]))
    candidates = [candidate for candidate in legal_values_dict_copy if
                  len(legal_values_dict_copy[candidate]) == len(legal_values_dict_copy[min_value_index])]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return highest_degree(vertices_degree, candidates)


def least_constraining_value(vertex, vertices_color_dict: dict, constraints_dict: dict, legal_values_dict: dict):
    lcv = None
    lcv_number_of_options = 0
    for color in legal_values_dict[vertex]:
        total_number_of_options = 0
        for constraint in constraints_dict[vertex]:
            if constraint in vertices_color_dict:
                continue
            available_values = len(legal_values_dict[constraint])
            if color in legal_values_dict[constraint]:
                available_values -= 1
            total_number_of_options += available_values
        if lcv is None or total_number_of_options > lcv_number_of_options:
            lcv = color
            lcv_number_of_options = total_number_of_options
    return lcv


def highest_degree(vertices_degree: dict, candidates: list):
    # returns the index(vertex) of the longest set (the most neighbors) in the graph
    return max(candidates, key=lambda candidate: vertices_degree[candidate])
