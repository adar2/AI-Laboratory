def absolute_distance_fitness(chromosome, target):
    chromosome.fitness = 0
    for i in range(len(target)):
        chromosome.fitness += abs(ord(chromosome.data[i]) - ord(target[i]))
