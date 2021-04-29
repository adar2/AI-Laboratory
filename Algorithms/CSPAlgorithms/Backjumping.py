from BaseCSPAlgorithm import BaseCSPAlgorithm
from Problems.AbstractProblem import AbstractProblem
from copy import copy
# --------------- TESTING PURPOSE ---------------------
from Problems.GraphColoringProblem import GraphColoringProblem
from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing


class BackJumpingAlgorithm(BaseCSPAlgorithm):
    def __init__(self, problem: AbstractProblem):
        super().__init__(problem)
        self.stack_depth_call = 0
        self.conflict_set_dict = None
        self.legal_values_dict = None

    def reset(self):
        self.conflict_set_dict = {key: set() for key in self.graph.keys()}
        self.vertices_color_dict = {}
        self.legal_values_dict = {key: set(color for color in self.color_groups_dict.keys()) for key in
                                  self.graph.keys()}
        for color_group in self.color_groups_dict.values():
            color_group.clear()

    # return whether some assignment is consistent with variable constraints or not
    def check_consistency(self, variable: int, color: int):
        for constraint in self.conflict_set_dict[variable]:
            if constraint in self.vertices_color_dict.keys() and self.vertices_color_dict[constraint] == color:
                return False
        return True

    def is_all_assigned(self):
        if len(self.vertices_color_dict) == self.problem.vertices:
            return True
        return False

    # method overriding
    def reset_vertex_assignment(self, vertex):
        super().reset_vertex_assignment(vertex)
        for conflict_set in self.conflict_set_dict.values():
            if vertex in conflict_set:
                conflict_set.remove(vertex)

    # method overriding
    def update_vertex(self, vertex, color):
        super().update_vertex(vertex, color)
        # update conflict set
        for constraint_vertex in self.constraints_dict[vertex]:
            self.conflict_set_dict[constraint_vertex].add(vertex)

    def mrv(self):
        candidate = None
        number_of_constraints = 0
        for vertex in self.graph.keys():
            if vertex in self.vertices_color_dict.keys():
                continue
            if len(self.conflict_set_dict[vertex]) > number_of_constraints or candidate is None:
                candidate = vertex
                number_of_constraints = len(self.constraints_dict[vertex])
        return candidate

    def run(self):
        while 1:
            # solution found break
            self.reset()
            self.backjumping_search(0)
            if self.is_complete():
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
        while color <= max(self.color_groups_dict.keys()):

            if self.check_consistency(vertex, color):
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
                    self.reset_vertex_assignment(vertex)
                    # recheck the current color to check if the new conflict set is affecting the assignment
                    color -= 1
                else:
                    return result, depth_call, conflict_set

            color += 1
        return False, depth_call, copy(self.conflict_set_dict[vertex])


if __name__ == '__main__':
    graph, vertices, edges = coloring_problem_file_parsing('le450_15a.col')
    p = GraphColoringProblem(graph, vertices, edges)
    a = BackJumpingAlgorithm(p)
    a.run()
