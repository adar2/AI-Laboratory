class Chromosome:
    def __init__(self, problem, data=None):
        if data is not None:
            self.data = data
        else:
            self.init_data()
        self.fitness = 0
        self.problem = problem

    def init_data(self):
        self.data = ''
