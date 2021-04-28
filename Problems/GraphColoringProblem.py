from AbstractProblem import AbstractProblem

class GraphColoringProblem(AbstractProblem):
    def __init__(self, graph: dict, vertices: int, edges: int):
        super().__init__()
        self.graph = graph
        self.vertices = vertices
        self.edges = edges
        self.density = self.calc_density()

    def get_search_space(self):
        return self.graph

    def printable_data(self, data: list = None):
        print(f'Number of vertices: {self.vertices}\n'
              f'Number of edges: {self.edges} \n'
              f'Edge density: {self.density}')

    def calc_density(self):
        return (2*self.edges) / (self.vertices * (self.vertices-1))