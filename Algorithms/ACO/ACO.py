from Utils.UtilFunctions import euc_distance
from Utils.CVRPFileParsing import parse_cvrp_file
from Problems.CVRP import CVRP
from os import getcwd
import random
import numpy
alpha = 2
beta = 5
sigm = 3
ro = 0.8
th = 80
COORDINATES = 0
DEMAND = 1


class ACO:
    def __init__(self, problem, max_iter, number_of_ants):
        self.problem = problem
        self.max_iter = max_iter
        self.number_of_ants = number_of_ants
        self.solutions = list()
        self.cities = {}
        self.demands = {}
        self.best_solution = None
        for i in range(len(self.problem.get_search_space())):
            self.cities[i+1] = self.problem.get_search_space()[i][COORDINATES]
            self.demands[i+1] = self.problem.get_search_space()[i][DEMAND]
        self.pheromones = {(city1, city2): 1 for city1 in self.cities for city2 in self.cities if city1 != city2}
        self.edges = {(city1, city2): euc_distance(self.cities[city1], self.cities[city2]) for city1 in self.cities for
                      city2 in self.cities}
        self.cities.pop(1)

    def __get_probabilities(self, city_index, cities):
        # probabilities = list(((self.pheromones[(min(x, city_index), max(x, city_index))]) ** alpha) * (
        #         (1 / self.edges[(min(x, city_index), max(x, city_index))]) ** beta) for x in cities)
        # prob_sum = sum(probabilities)
        # probabilities = [prob / prob_sum for prob in probabilities]
        probabilities = list(map(lambda x: ((self.pheromones[(min(x, city_index), max(x, city_index))]) ** alpha) * (
                    (1 / self.edges[(min(x, city_index), max(x, city_index))]) ** beta), cities))
        probabilities = probabilities / numpy.sum(probabilities)
        return probabilities

    def find_solution(self):
        solution = list()
        cities = self.cities.copy()
        capacity_limit = self.problem.capacity
        while len(cities) != 0:
            path = list()
            city_index = random.choice(list(cities.keys()))
            city = self.cities[city_index]
            capacity = capacity_limit - self.demands[city_index]
            path.append(city)
            cities.pop(city_index)
            while len(cities) != 0:
                probabilities = self.__get_probabilities(city_index, cities)
                city_index = random.choices(list(cities.keys()), probabilities)[0]
                city = self.cities[city_index]
                capacity = capacity - self.demands[city_index]
                if capacity > 0:
                    path.append(city)
                    cities.pop(city_index)
                else:
                    break
            solution.append(path)
        return solution

    def calc_solution_cost(self, solution, edges):
        solution_cost = 0
        depot = 1
        for truck in solution:
            last_city = depot
            for current_city in truck:
                current_city_index = list(self.cities.values()).index(current_city)
                solution_cost += self.edges[(min(last_city, current_city_index), max(last_city, current_city_index))]
                last_city = current_city_index
            solution_cost += edges[(min(last_city, depot), max(last_city, depot))]
        return solution_cost

    def update_pheromone(self):
        avg = sum((solution[1] for solution in self.solutions)) / len(self.solutions)
        self.pheromones = {k: (ro + th / avg) * v for (k, v) in self.pheromones.items()}
        self.solutions.sort(key=lambda x: x[1])
        if self.best_solution is not None:
            if self.solutions[0][1] < self.best_solution[1]:
                self.best_solution = self.solutions[0]
            for path in self.best_solution[0]:
                for i in range(len(path) - 1):
                    current_city_index = list(self.cities.values()).index(path[i])
                    next_city_index = list(self.cities.values()).index(path[i + 1])
                    self.pheromones[(min(current_city_index,next_city_index), max(current_city_index,next_city_index))] = sigm / self.best_solution[1] + \
                                                                                        self.pheromones[(min(current_city_index,next_city_index), max(current_city_index,next_city_index))]
        else:
            self.best_solution = self.solutions[0]
        for l in range(sigm):
            paths = self.solutions[l][0]
            L = self.solutions[l][1]
            for path in paths:
                for i in range(len(path) - 1):
                    current_city_index = list(self.cities.values()).index(path[i])
                    next_city_index = list(self.cities.values()).index(path[i+1])
                    self.pheromones[(min(current_city_index,next_city_index), max(current_city_index,next_city_index))] = (sigm - (l + 1) / L ** (
                            l + 1)) + self.pheromones[(min(current_city_index,next_city_index), max(current_city_index,next_city_index))]
        return self.best_solution

    def run(self):
        for i in range(self.max_iter):
            self.solutions = list()
            for _ in range(self.number_of_ants):
                solution = self.find_solution()
                self.solutions.append((solution, self.calc_solution_cost(solution, self.edges)))
            self.best_solution = self.update_pheromone()
            print(str(i) + ":\t" + str(int(self.best_solution[1])))
        return self.best_solution


if __name__ == '__main__':
    max_i = 3
    capacity, locations = parse_cvrp_file(getcwd() + '\E-n22-k4.txt')
    p = CVRP(capacity, locations)
    s = ACO(p,1000,22)
    s.run()