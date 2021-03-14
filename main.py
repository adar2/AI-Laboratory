from SimpleGeneticAlgorithm import SimpleGeneticAlgorithm
from FitnessFunctions import absolute_distance_fitness as fitness_func
from MatingFunctions import uniform_point_crossover as mating_func

if __name__ == '__main__':
    algo = SimpleGeneticAlgorithm(2048, 16384, .1, .25, "Hello world!", fitness_func,
                                  mating_func)
    algo.run()
