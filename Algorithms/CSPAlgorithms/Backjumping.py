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

    def run(self):
        while 1:
            # solution found break
            if self.is_complete():
                break
            self.backjumping_search(0)
            self.generate_another_color()
        print(f'Number of colors {len(self.color_groups_dict)}')

    def backjumping_search(self, depth_call: int):
        # check for stop case
        if self.is_complete():
            return True, depth_call, []  # stop the algorithm and do something
        vertex = self.select_unassigned_variable()
        for color in self.color_groups_dict.keys():
            if self.check_consistency(vertex, color):
                self.update_vertex(vertex, color)
                result, _, conflict_set = self.backjumping_search(depth_call + 1)
                if result:
                    return result, depth_call, conflict_set
                # do the backjumping part here
                # assuming deepest vertex in the conflict set
                if vertex in conflict_set:
                    # update vertex conflict set
                    conflict_set.remove(vertex)
                    self.constraints_dict[vertex].union(conflict_set)
                    # self.reset_vertex_assignment(vertex)
                else:
                    return result, depth_call, conflict_set

        return False, depth_call, copy(self.constraints_dict[vertex])


if __name__ == '__main__':
    graph, vertices, edges = coloring_problem_file_parsing('le450_15a.col')
    p = GraphColoringProblem(graph, vertices, edges)
    a = BackJumpingAlgorithm(p)
    a.run()
