from SimpleGeneticAlgorithm import SimpleGeneticAlgorithm
from FitnessFunctions import absolute_distance_fitness
from MatingFunctions import single_point_crossover

if __name__ == '__main__':
    algo = SimpleGeneticAlgorithm(2048, 16384, .1, .25, "Hello world!", absolute_distance_fitness,
                                  single_point_crossover)
    algo.run()
