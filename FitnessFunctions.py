
def absolute_distance_fitness(chromosome, target):
    for i in range(len(target)):
        chromosome.fitness += abs(chromosome.data[i] - target[i])