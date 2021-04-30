from BaseCSPAlgorithm import BaseCSPAlgorithm
from Problems.AbstractProblem import AbstractProblem
from copy import copy
from Algorithms.CSPAlgorithms.Heuristics import minimum_remaining_values as mrv
# --------------- TESTING PURPOSE ---------------------
from Problems.GraphColoringProblem import GraphColoringProblem
from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing


class BackJumpingAlgorithm(BaseCSPAlgorithm):
    def __init__(self, problem: AbstractProblem):
        super().__init__(problem)
        self.stack_depth_call = 0
        self.conflict_set_dict = None

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
        while 1:
            self.reset()
            self.backjumping_search(0)
            if self.is_complete():
                # solution found break
                break
            self.generate_another_color()
        print(f'Found legal graph coloring with {len(self.color_groups_dict)} colors ')

    def backjumping_search(self, depth_call: int):
        # check whether all vertices has been assigned with color
        if self.is_all_assigned():
            return True, depth_call, set()  # stop the algorithm and return

        vertex = self.select_unassigned_variable()
        print(f'Current vertex : {vertex} ,Depth call : {depth_call} '
              f',Number of assigned vertices : {len(self.vertices_color_dict)} '
              f', Number of colors : {len(self.color_groups_dict)}')

        color = 1
        while color <= max(self.color_groups_dict) and len(self.domains_dict[vertex]) > 0:

            if self.check_consistency(vertex, color) or vertex in self.vertices_color_dict:
                if vertex not in self.vertices_color_dict:
                    self.update_vertex(vertex, color)

                result, _, conflict_set = self.backjumping_search(depth_call + 1)
                if result:
                    return result, depth_call, conflict_set

                # backjump until finding vertex contained in the conflict list
                # assuming deepest vertex in the conflict set

                if vertex in conflict_set:
                    # update vertex conflict set
                    conflict_set.remove(vertex)
                    self.conflict_set_dict[vertex] = self.conflict_set_dict[vertex].union(conflict_set)
                else:
                    return result, depth_call, conflict_set

            color += 1
        return False, depth_call, copy(self.conflict_set_dict[vertex])


if __name__ == '__main__':
    graph, vertices, edges = coloring_problem_file_parsing('le450_15a.col')
    p = GraphColoringProblem(graph, vertices, edges)
    a = BackJumpingAlgorithm(p)
    a.run()
