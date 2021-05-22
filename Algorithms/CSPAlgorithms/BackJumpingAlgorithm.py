from copy import copy

from Algorithms.CSPAlgorithms.BaseCSPAlgorithm import BaseCSPAlgorithm
from Problems.AbstractProblem import AbstractProblem
from time import process_time


class BackJumpingAlgorithm(BaseCSPAlgorithm):
    def __init__(self, problem: AbstractProblem):
        super().__init__(problem)
        self.conflict_set_dict = None
        self.states_explored = 0

    def reset(self):
        self.conflict_set_dict = {key: set() for key in self.graph.keys()}
        self.vertices_color_dict = {}
        self.domains_dict = self.generate_domains_dict(self.current_color)
        for color_group in self.color_groups_dict.values():
            color_group.clear()

    # return whether some assignment is consistent with variable constraints or not
    def check_consistency(self, vertex: int, color: int):
        for conf_vertex in self.conflict_set_dict[vertex]:
            if conf_vertex in self.vertices_color_dict.keys() and self.vertices_color_dict[conf_vertex] == color:
                return False
        return True

    def is_all_assigned(self):
        if len(self.vertices_color_dict) == self.problem.vertices:
            return True
        return False

    # method overriding
    def reset_vertex_assignment(self, vertex_1):
        for vertex_2 in self.graph:
            if vertex_1 in self.conflict_set_dict[vertex_2]:
                flag = True  # if the current vertex is the only conflict
                self.conflict_set_dict[vertex_2].remove(vertex_1)
                vertex_color = self.vertices_color_dict[vertex_1]
                # check whether the vertex_1 color is now available for vertex_2
                for conflict in self.conflict_set_dict[vertex_2]:
                    if self.vertices_color_dict[conflict] == vertex_color:
                        flag = False
                        break
                if flag:
                    self.domains_dict[vertex_2].append(vertex_color)
        super().reset_vertex_assignment(vertex_1)

    # method overriding
    def update_vertex(self, vertex, color):
        super().update_vertex(vertex, color)
        # update conflict set
        for constraint_vertex in self.constraints_dict[vertex]:
            self.conflict_set_dict[constraint_vertex].add(vertex)
            if color in self.domains_dict[constraint_vertex]:
                self.domains_dict[constraint_vertex].remove(color)

    def run(self):
        print('Executing ...')
        start_time = process_time()
        highest_degree = self.get_highest_degree_in_graph()
        while self.current_color < highest_degree:
            self.reset()
            if self.backjumping_search() and self.is_complete():
                # solution found break
                break
            self.generate_another_color()
        self.elapsed_time = round(process_time()-start_time,2)
        print("---------------------")
        print(f'Chromatic number found: {len(self.color_groups_dict)}')
        print(f'Number of states explored: {self.states_explored}')
        print(f"Time elapsed: {self.elapsed_time}")
        return len(self.color_groups_dict)

    def backjumping_search(self):
        # check whether all vertices has been assigned with color
        if self.is_all_assigned():
            return True, set()  # stop the algorithm and return

        vertex = self.select_unassigned_vertex()

        color = self.select_value_for_vertex(vertex)

        self.states_explored += 1

        if self.check_consistency(vertex, color):
            if vertex not in self.vertices_color_dict:
                self.update_vertex(vertex, color)

            result, conflict_set = self.backjumping_search()
            if result:
                return result, conflict_set

            # backjump until finding vertex contained in the conflict list
            # assuming deepest vertex in the conflict set

            if vertex in conflict_set:
                # update vertex conflict set
                conflict_set.remove(vertex)
                self.conflict_set_dict[vertex] = self.conflict_set_dict[vertex].union(conflict_set)
            else:
                return result, conflict_set

        if vertex in self.vertices_color_dict:
            self.reset_vertex_assignment(vertex)
        return False, copy(self.conflict_set_dict[vertex])
