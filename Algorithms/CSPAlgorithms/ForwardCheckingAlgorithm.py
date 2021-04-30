from BaseCSPAlgorithm import BaseCSPAlgorithm
from Problems.AbstractProblem import AbstractProblem
from random import choice
from copy import copy
from queue import Queue
from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing
from Problems.GraphColoringProblem import GraphColoringProblem


class ForwardCheckingAlgorithm(BaseCSPAlgorithm):
    def __init__(self, problem: AbstractProblem) -> None:
        super().__init__(problem)
        self.max_coloring = self.get_highest_degree_in_graph() + 1
        self.arcs_queue = self.generate_arcs_queue()
        self.domains_dict = self.generate_domains_dict(self.max_coloring)

    def run(self):
        current_coloring = 2
        while current_coloring < self.max_coloring:
            self.reset(current_coloring)
            if not self.is_coloring_possible(current_coloring):
                print(f'Coloring with {current_coloring} colors FAILED!')
                current_coloring += 1
            else:
                print(f'Coloring with {current_coloring} colors succeeded!')
                current_coloring -= 1
                break
        print(f'Chromatic number: {current_coloring}')
        return current_coloring

    def is_arc_consistent(self, domains_dict):
        temp_arcs_queue = self.generate_arcs_queue()
        while not temp_arcs_queue.empty():
            # if self.is_empty_domain_exists(domains_dict):
            #     return False, domains_dict
            current_arc = temp_arcs_queue.get()  # returns a tuple x,y
            if self.remove_incosistent_items(current_arc, domains_dict):
                for neighbour in self.get_all_neighbours_of_vertex(current_arc[0]):
                    temp_arcs_queue.put(neighbour)
        return not self.is_empty_domain_exists(domains_dict), domains_dict

    def is_coloring_possible(self, current_coloring):
        self.domains_dict = self.generate_domains_dict(current_coloring)
        while not self.is_complete():
            vertex = self.select_unassigned_vertex()
            if len(self.domains_dict[vertex]) == 0:
                return False
            color = choice(self.domains_dict[vertex])
            success, updated_domain = self.forward_check(vertex, color, copy(self.domains_dict))
            while not success:
                self.domains_dict[vertex].remove(color)
                if len(self.domains_dict[vertex]) == 0:
                    return False
                color = choice(self.domains_dict[vertex])
                success, updated_domain = self.forward_check(vertex, color, copy(self.domains_dict))
            self.update_vertex(vertex, color)
            self.domains_dict = updated_domain
        return True

    def forward_check(self, vertex, color, copied_domains_dict):
        self.update_vertex(vertex, color)
        copied_domains_dict[vertex] = [color]
        success, updated_domain = self.is_arc_consistent(copied_domains_dict)
        self.reset_vertex_assignment(vertex)
        return success, updated_domain

    def remove_incosistent_items(self, current_arc, domains_dict):
        removed = False
        vertex_1 = current_arc[0]
        vertex_2 = current_arc[1]
        for color in domains_dict[vertex_1]:
            vertex_2_colors = copy(domains_dict[vertex_2])
            if len(vertex_2_colors) == 0:
                continue
            if color in vertex_2_colors:
                vertex_2_colors.remove(color)
            # if we removed the color from vertex_2's domain and there is at least one other value remaining -
            # it means that there is a value that satisfies the constraint (that value != color)
            if len(vertex_2_colors) == 0:
                domains_dict[vertex_1].remove(color)
                removed = True
        return removed

    def is_empty_domain_exists(self, temp_domains_dict):
        for vertex in temp_domains_dict:
            if len(temp_domains_dict[vertex]) == 0:
                return True
        return False

    def generate_arcs_queue(self):
        arcs_queue = Queue()
        for vertex in self.graph:
            for vertex_2 in self.graph[vertex]:
                arcs_queue.put((vertex, vertex_2))
        return arcs_queue

    def get_all_neighbours_of_vertex(self, vertex):
        neighbours = []
        for vertex in self.graph:
            for vertex_2 in self.graph[vertex]:
                if vertex_2 == vertex:
                    neighbours.append((vertex, vertex_2))
        return neighbours

    def reset(self, coloring):
        self.vertices_color_dict = {}
        for color_group in self.color_groups_dict.values():
            color_group.clear()
        self.arcs_queue = self.generate_arcs_queue()
        self.domains_dict = self.generate_domains_dict(coloring)


if __name__ == '__main__':
    graph, vertices, edges = coloring_problem_file_parsing('le450_15a.col')
    problem = GraphColoringProblem(graph, vertices, edges)
    algo = ForwardCheckingAlgorithm(problem)
    algo.run()
