from Problems.AbstractProblem import AbstractProblem
from Utils.Constants import DEMAND, COORDINATES


class CVRP(AbstractProblem):
    def __init__(self, vehicle_capacity: int, locations: list):
        super().__init__()
        self.capacity = vehicle_capacity
        self.locations = locations
        self.cities_dict = self.__generate_cities_dict()

    def get_search_space(self):
        return self.locations

    def printable_data(self, data: list):
        trucks = self.generate_truck_partition(data)
        printable_trucks_list = []
        # convert city coordinates to city index
        for truck in trucks:
            printable_trucks_list.append([self.cities_dict[city[COORDINATES]] for city in truck])
        # add depot at the beginning of first truck's route and at the end of the last truck's route
        if printable_trucks_list[0][0] != 0:
            printable_trucks_list[0].insert(0, 0)
        printable_trucks_list[-1].append(0)
        # construct final printable format
        printable_data = ""
        for i in range(len(printable_trucks_list)):
            printable_data += f"\nTruck {i + 1}: {printable_trucks_list[i]}"
        return printable_data

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

    def __generate_cities_dict(self):
        cities = {}
        for i in range(len(self.get_search_space())):
            cities[(self.get_search_space()[i][COORDINATES])] = i
        return cities
