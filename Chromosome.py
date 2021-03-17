class Chromosome:
    def __init__(self, problem):
        self.data = ''
        self.fitness = 0
        self.problem = problem

    def init_data(self):
        self.data = ''
