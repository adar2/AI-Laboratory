from AbstractProblem import AbstractProblem


class CVRP(AbstractProblem):
    def __init__(self, vehicle_capacity: int, locations: list):
        super().__init__()
        self.capacity = vehicle_capacity
        self.locations = locations

    def get_search_space(self):
        return self.locations

    def printable_data(self, data: list):
        pass
