from Algorithms.GeneticAlgorithm.GeneticAlgorithmBase import GeneticAlgorithmBase
from Utils.Constants import MUTATION_RATE, ELITE_RATE
from time import time
from Problems.KnapSack import KnapSack


class GeneralGeneticAlgorithm(GeneticAlgorithmBase):
    def __init__(self, pop_size, max_iter, problem, fitness_function=None, mating_function=None, mutation_function=None,
                 selection_function=None, survival_function=None, mutation_rate=MUTATION_RATE, elite_rate=ELITE_RATE):
        super().__init__(pop_size, max_iter, problem, fitness_function, mating_function, mutation_function, selection_function,
                         survival_function, mutation_rate, elite_rate)

    def run(self):
        last_best = None
        stuck_counter = 0
        start_time = time()
        self.init_population()
        for i in range(self.max_iter):
            print(f"current iteration : {i + 1}")
            self.number_of_iterations += 1
            self.calc_fitness()
            self.best = min(self.population, key=lambda x: x.fitness)
            self.print_current_state()
            self.iterations_costs.append(self.best.fitness)
            self.current_time = time()
            stuck_counter, last_best = self.update_stuck_counter(last_best, stuck_counter)
            # goal test
            # knapsack goal test
            if isinstance(self.problem, KnapSack):
                if self.knapsack_check():
                    self.solved = True
                    break
            # regular goal test
            else:
                if self.is_solved_or_stuck(stuck_counter):
                    self.solved = True
                    break
            eligible_parents = self.select_parents()
            if eligible_parents is None or len(eligible_parents) == 0:
                continue
            survivors = self.survival_function(self.population, self.elite_rate)
            self.mate(eligible_parents, survivors)
            self.swap()
            self.increase_age()
        self.update_time_stats(start_time)
        print(f"Time elapsed {self.elapsed_time}")
        return self.best
