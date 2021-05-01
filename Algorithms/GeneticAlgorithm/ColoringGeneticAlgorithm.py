from Algorithms.GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithmBase
from Utils.Constants import MUTATION_RATE, ELITE_RATE
from time import time
from Problems.GraphColoringProblem import GraphColoringProblem
from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing
from random import randint
from Algorithms.GeneticAlgorithm.MutateFunctions import coloring_mutation
from Algorithms.GeneticAlgorithm.MatingFunctions import single_point_crossover
from Algorithms.GeneticAlgorithm.SelectionFunctions import truncation_selection
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_elite
from random import random, choice


# TODO: mutation function, choose correct operator -> single point, decreasing coloring -> implement functions, chromosome init data
class ColoringGeneticAlgorithm(GeneticAlgorithmBase):
    def __init__(self, pop_size, max_iter, problem, fitness_function=None, mutation_rate=MUTATION_RATE, elite_rate=ELITE_RATE):
        super().__init__(pop_size, max_iter, problem, fitness_function, mutation_rate, elite_rate)
        self.current_coloring = self.problem.get_max_degree() + 1  # upper bound of coloring in any graph
        self.bad_edges_dict = {}
        self.mating_function = single_point_crossover
        self.selection_function = truncation_selection
        self.survival_function = survival_of_the_elite
        self.mutation_function = coloring_mutation
        self.constraints_dict = self.problem.get_search_space()
        self.graph = self.problem.get_search_space()

    def run(self):
        last_best = None
        stuck_counter = 0
        start_time = time()
        self.init_population()
        for i in range(self.max_iter):
            self.number_of_iterations += 1
            self.update_bad_edges()
            self.calc_fitness()
            self.best = min(self.population, key=lambda x: x.fitness)
            self.print_current_state()
            self.iterations_costs.append(self.best.fitness)
            self.current_time = time()
            stuck_counter, last_best = self.update_stuck_counter(last_best, stuck_counter)
            # goal test
            if self.is_solved():
                self.update_coloring()
                continue
            if self.is_stuck(stuck_counter):
                self.solved = True
                break
            eligible_parents = self.select_parents()
            if eligible_parents is None or len(eligible_parents) == 0:
                continue
            survivors = self.survival_function(self.population, self.elite_rate)
            self.coloring_mate(eligible_parents, survivors, self.current_coloring, self.bad_edges_dict)
            self.swap()
            self.increase_age()
        self.update_time_stats(start_time)
        print(f"Time elapsed {self.elapsed_time}")
        return self.best

    def is_stuck(self, stuck_counter):
        raise NotImplementedError

    def coloring_mate(self, eligible_parents, survivors, current_coloring, bad_edges_dict):
        number_of_offsprings = self.pop_size - len(survivors)
        self.buffer = survivors
        for i in range(number_of_offsprings):
            parent_1 = choice(eligible_parents)
            parent_2 = choice(eligible_parents)
            child = self.mating_function(parent_1, parent_2)
            if random() < MUTATION_RATE:
                self.mutation_function(child, current_coloring, bad_edges_dict)
            self.buffer.append(child)
    def update_bad_edges(self):
        for chromosome in self.population:
            bad_edges = []
            data = chromosome.data
            for vertex in range(len(data)):
                for constraint_vertex in self.constraints_dict[vertex + 1]:
                    if data[vertex] == data[constraint_vertex - 1]:
                        bad_edges.append((vertex, constraint_vertex - 1))
            self.bad_edges_dict[chromosome] = bad_edges

    def is_solved(self):
        if self.best.fitness == 0:
            return True
        return False

    def update_coloring(self):
        self.current_coloring = -1
        for chromosome in self.population:
            data = chromosome.data
            for vertex in range(len(data)):
                if data[vertex] > self.current_coloring:
                    data[vertex] = randint(1, self.current_coloring + 1)
            chromosome.data = data


if __name__ == '__main__':
    graph, vertices, edges = coloring_problem_file_parsing('huck.col')
    p = GraphColoringProblem(graph, vertices, edges)
    a = ColoringGeneticAlgorithm(50, 50, p)
    a.run()
