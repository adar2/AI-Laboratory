from Algorithms.GeneticAlgorithm.Chromosome import Chromosome
from Problems.AbstractProblem import AbstractProblem


class NSGAChromosome(Chromosome):
    def __init__(self, problem: AbstractProblem, data=None):
        super().__init__(problem, data)
        self.trucks_objective = 0
        self.route_objective = 0
        self.crowding_distance = 0
        self.front = 0
        self.dominated_chromosomes_list = set()
        self.domination_counter = 0

    # Domination operator
    def __gt__(self, other_chromosome):
        return (self.trucks_objective < other_chromosome.trucks_objective and self.route_objective <= other_chromosome.route_objective) \
               or (
               self.trucks_objective <= other_chromosome.trucks_objective and self.route_objective <= other_chromosome.route_objective)
