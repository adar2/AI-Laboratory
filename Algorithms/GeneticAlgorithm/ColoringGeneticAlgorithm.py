from Algorithms.GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithmBase
from Utils.Constants import MUTATION_RATE, ELITE_RATE, STUCK_PCT
from time import time
from Problems.GraphColoringProblem import GraphColoringProblem
from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing
from random import randint
from Algorithms.GeneticAlgorithm.MutateFunctions import coloring_mutation
from Algorithms.GeneticAlgorithm.MatingFunctions import uniform_point_crossover as imported_crossover
from Algorithms.GeneticAlgorithm.SelectionFunctions import truncation_selection as imported_selection
from Algorithms.GeneticAlgorithm.SurvivalFunctions import survival_of_the_young as imported_survival
from Algorithms.GeneticAlgorithm.FitnessFunctions import graph_coloring_fitness
from random import random, choice


# TODO: mutation function, choose correct operator -> single point, decreasing coloring -> implement functions, chromosome init data
class ColoringGeneticAlgorithm(GeneticAlgorithmBase):

    def __init__(self, pop_size, max_iter, problem, fitness_function=None, mutation_rate=MUTATION_RATE, elite_rate=ELITE_RATE):
        super().__init__(pop_size, max_iter, problem, fitness_function, mutation_rate, elite_rate)
        self.current_coloring = self.problem.get_max_degree() + 1  # upper bound of coloring in any graph
        self.bad_edges_dict = {}
        self.mating_function = imported_crossover
        self.selection_function = imported_selection
        self.survival_function = imported_survival
        self.mutation_function = coloring_mutation
        self.fitness_function = graph_coloring_fitness
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
        print("-----------------------------------")
        print(f"Time elapsed: {self.elapsed_time}")
        print(f"Chromatic Number: {self.current_coloring + 1}")
        return self.best

    def is_stuck(self, stuck_counter):
        return (stuck_counter / self.max_iter) >= STUCK_PCT

    def coloring_mate(self, eligible_parents, survivors, current_coloring, bad_edges_dict):
        number_of_offsprings = self.pop_size - len(survivors)
        self.buffer = survivors
        for i in range(number_of_offsprings):
            parent_1 = choice(eligible_parents)
            parent_2 = choice(eligible_parents)
            child = self.mating_function(parent_1, parent_2)
            child_bad_edges = self.__get_bad_edges(child)
            if random() < MUTATION_RATE:
                self.mutation_function(child, current_coloring, child_bad_edges)
            self.buffer.append(child)

    def update_bad_edges(self):
        self.bad_edges_dict.clear()
        for chromosome in self.population:
            bad_edges = []
            data = chromosome.data
            for vertex in range(len(data)):
                for constraint_vertex in self.constraints_dict[vertex + 1]:
                    # avoid adding the bad edge from both sides
                    if data[vertex] == data[constraint_vertex - 1] and (constraint_vertex - 1, vertex) not in bad_edges:
                        bad_edges.append((vertex, constraint_vertex - 1))
            self.bad_edges_dict[chromosome] = bad_edges

    def is_solved(self):
        if self.best.fitness == 0:
            return True
        return False

    def update_coloring(self):
        self.current_coloring -= 1
        for chromosome in self.population:
            data = chromosome.data
            for vertex in range(len(data)):
                if data[vertex] > self.current_coloring:
                    data[vertex] = randint(1, self.current_coloring + 1)
            chromosome.data = data

    def calc_fitness(self):
        avg_fitness = 0
        standard_dev = 0
        for chromosome in self.population:
            bad_edges = self.bad_edges_dict[chromosome]
            self.fitness_function(chromosome, bad_edges)
        avg_fitness, standard_dev = self.calc_stats(avg_fitness, standard_dev)
        print(f"Average fitness: {avg_fitness}")
        # print(f"Standard Deviation: {standard_dev}")

    def __get_bad_edges(self, chromosome):
        bad_edges = []
        data = chromosome.data
        for vertex in range(len(data)):
            for constraint_vertex in self.constraints_dict[vertex + 1]:
                # avoid adding the bad edge from both sides
                if data[vertex] == data[constraint_vertex - 1] and (constraint_vertex - 1, vertex) not in bad_edges:
                    bad_edges.append((vertex, constraint_vertex - 1))
        return bad_edges

    def print_current_state(self):
        print(f'Current Coloring: {self.current_coloring}')
        print(f'Current Best Fitness: {self.best.fitness}')


if __name__ == '__main__':
    graph, vertices, edges = coloring_problem_file_parsing('le450_15a.col')
    p = GraphColoringProblem(graph, vertices, edges)
    a = ColoringGeneticAlgorithm(50, 1000, p)
    a.run()
