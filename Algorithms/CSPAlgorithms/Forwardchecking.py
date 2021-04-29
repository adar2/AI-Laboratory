from BaseCSPAlgorithm import BaseCSPAlgorithm
from Problems.AbstractProblem import AbstractProblem
from random import choice
from copy import copy
from queue import Queue


class ForwardChecking(BaseCSPAlgorithm):
    def __init__(self, problem: AbstractProblem) -> None:
        super().__init__(problem)
        self.max_coloring = self.get_highest_degree_in_graph() + 1
        self.arcs_queue = self.generate_arcs_queue()

    def run(self):
        current_coloring = self.max_coloring
        while current_coloring > 0:
            if not self.is_coloring_possible(current_coloring):
                break
            current_coloring -= 1
            print(f'Coloring {current_coloring} succeeded!')
        return current_coloring

    def is_arc_consistent(self, domains_dict):
        temp_domains_dict = copy(domains_dict)
        temp_arcs_queue = copy(self.arcs_queue)
        while not temp_arcs_queue.empty():
            current_arc = temp_arcs_queue.get()  # returns a tuple x,y
            if self.remove_incosistent_items(current_arc, temp_domains_dict):
                for neighbour in self.get_all_neighbours_of_vertex(current_arc[0]):
                    temp_arcs_queue.put(neighbour)
        return self.is_empty_domain_exists(temp_domains_dict), temp_domains_dict

    def generate_domains_dict(self, max_coloring):
        domains_dict = {}
        for vertex in self.graph:
            domains_dict[vertex] = range(1, max_coloring + 1)
        return domains_dict

    def is_coloring_possible(self, current_coloring):
        domains_dict = self.generate_domains_dict(current_coloring)
        while not self.is_complete():
            vertex = self.select_unassigned_variable()
            try:
                color = choice(domains_dict[vertex])
                success, updated_domain = self.forward_check(vertex, color, domains_dict)
                while not success:
                    if len(domains_dict[vertex]) == 0:
                        return False
                    domains_dict[vertex].remove(color)
                    color = choice(domains_dict[vertex])
                    success, updated_domain = self.forward_check(vertex, color, domains_dict)
                self.update_vertex(vertex, color)
                domains_dict = updated_domain
            except:
                return False

    def forward_check(self, vertex, color, domains_dict):
        self.update_vertex(vertex, color)
        success, updated_domain = self.is_arc_consistent(domains_dict)
        self.reset_vertex_assignment(vertex)
        return success, updated_domain

    def remove_incosistent_items(self, current_arc, domains_dict):
        removed = False
        vertex_1 = current_arc[0]
        vertex_2 = current_arc[1]
        for color in domains_dict[vertex_1]:
            vertex_2_colors = domains_dict[vertex_2]
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
                arcs_queue.put((vertex,vertex_2))
        return arcs_queue

    def get_all_neighbours_of_vertex(self, vertex):
        neighbours = []
        for vertex in self.graph:
            for vertex_2 in self.graph[vertex]:
                if vertex_2 == vertex:
                    neighbours.append((vertex,vertex_2))
        return neighbours

