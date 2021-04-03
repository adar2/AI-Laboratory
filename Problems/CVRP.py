from Problems.AbstractProblem import AbstractProblem
from Utils.Constants import DEMAND


class CVRP(AbstractProblem):
    def __init__(self, vehicle_capacity: int, locations: list):
        super().__init__()
        self.capacity = vehicle_capacity
        self.locations = locations

    def get_search_space(self):
        return self.locations

    def printable_data(self, data: list):
        return data

    def generate_truck_partition(self, locations: list):
        data = [[]]
        index = 0
        current_capacity = 0
        for item in locations:
            data[index].append(item)
            current_capacity += item[DEMAND]
            if current_capacity > self.capacity:
                data[index].remove(item)
                index += 1
                data.append([])
                data[index].append(item)
                current_capacity = item[DEMAND]
        return data

