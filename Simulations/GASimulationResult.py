from statistics import mean


class GASimulationResult:

    def __init__(self, size, problem, fitness_function,
                 mating_function, mutation_function, selection_function, survival_function,
                 mutation_rate, elite_rate, iterations, runtimes) -> None:
        self.selection_function = selection_function
        self.survival_function = survival_function
        self.elite_rate = elite_rate
        self.mutation_function = mutation_function
        self.mutation_rate = mutation_rate
        self.mating_function = mating_function
        self.fitness_function = fitness_function
        self.size = size
        self.problem = problem
        if iterations is not None:
            if len(iterations) > 0:
                self.iterations_mean = mean(iterations)
            else:
                self.iterations_mean = 0
        else:
            self.iterations_mean = 0
        self.iterations_data = iterations
        if runtimes is not None:
            if len(runtimes) > 0:
                self.runtime_mean = mean(runtimes)
            else:
                self.runtime_mean = 0
        else:
            self.runtime_mean = 0
        self.runtime_data = runtimes

    def __str__(self) -> str:
        return f'Population Size: {self.size}\n' \
               f'Elite Pct: {self.elite_rate} \n' \
               f'Mutation Rate: {self.mutation_rate} \n' \
               f'Selection Strategy: {self.get_func_name(self.selection_function)} \n' \
               f'Survival Strategy: {self.get_func_name(self.survival_function)} \n' \
               f'Mutation Strategy: {self.get_func_name(self.mutation_function)} \n' \
               f'Fitness Function: {self.get_func_name(self.fitness_function)} \n' \
               f'Mating Strategy: {self.get_func_name(self.mating_function)}'

    def get_func_name(self, function):
        name = function.__name__
        name = name.replace('_', ' ')
        if name == "survival of the elite":
            name = "elitism"
        elif name == "survival of the young":
            name = "age-based"
        return name
