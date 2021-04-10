import random
import time
from Utils.Constants import COORDINATES, DEMAND, ACO_ALPHA, ACO_BETA, ACO_TAU, ACO_RO, ACO_SIGMA,STUCK_PCT
from Utils.UtilFunctions import euc_distance
from Utils.Constants import CLOCK_RATE


class ACO:
    def __init__(self, problem, max_iter, number_of_ants):
        # algorithm problem
        self.problem = problem
        # maximum iterations
        self.max_iter = max_iter
        # number of ants in colony
        self.number_of_ants = number_of_ants
        # ants solutions list
        self.solutions = list()
        # dictionary of cities where the key is the index of the city and the value is the city coordinates
        self.cities = {}
        # dictionary of cities demands where the city index is the key and the demand is the value
        self.demands = {}
        # colony best solution tuple (solution, solution cost)
        self.best_solution = None
        # init the dictionaries
        for i in range(len(self.problem.get_search_space())):
            self.cities[i + 1] = self.problem.get_search_space()[i][COORDINATES]
            self.demands[i + 1] = self.problem.get_search_space()[i][DEMAND]
        # dictionary of pheromones where the key is the edge (i,j) and the value is 1
        self.pheromones = {(city1, city2): 1 for city1 in self.cities for city2 in self.cities if city1 != city2}
        # dictionary of costs where the key is the edge (i,j) and the value is the distance between city i and city j
        self.edges = {(city1, city2): euc_distance(self.cities[city1], self.cities[city2]) for city1 in self.cities for
                      city2 in self.cities}
        # remove the depot city index from the cities dict
        self.cities.pop(1)
        # time elapsed from the beginning of run
        self.elapsed_time = 0
        self.clock_ticks = 0
        self.iterations_cost = []

    # calculate each city probability to be chosen next by the formula
    def __get_probabilities(self, city_index, cities):
        probabilities = list(
            ((self.pheromones[(min(other_city_index, city_index), max(other_city_index, city_index))]) ** ACO_ALPHA) * (
                    (1 / self.edges[
                        (min(other_city_index, city_index), max(other_city_index, city_index))]) ** ACO_BETA) for
            other_city_index in cities)
        prob_sum = sum(probabilities)
        probabilities = [prob / prob_sum for prob in probabilities]
        return probabilities

    # generate ant solution using the probability function
    def find_solution(self):
        solution = list()
        cities = self.cities.copy()
        capacity_limit = self.problem.capacity
        while len(cities) != 0:
            path = list()
            city_index = random.choice(list(cities.keys()))
            capacity = capacity_limit - self.demands[city_index]
            path.append(city_index)
            cities.pop(city_index)
            while len(cities) != 0:
                probabilities = self.__get_probabilities(city_index, cities)
                city_index = random.choices(list(cities.keys()), probabilities)[0]
                capacity = capacity - self.demands[city_index]
                if capacity > 0:
                    path.append(city_index)
                    cities.pop(city_index)
                else:
                    break
            solution.append(path)
        return solution

    # calculate an ant solution cost
    def calc_solution_cost(self, solution, edges):
        solution_cost = 0
        depot = 1
        for truck in solution:
            last_city = depot
            for current_city in truck:
                solution_cost += self.edges[(min(last_city, current_city), max(last_city, current_city))]
                last_city = current_city
            solution_cost += edges[(min(last_city, depot), max(last_city, depot))]
        return solution_cost

    # update the pheromone dictionary by the formula
    def update_pheromone(self):
        avg = sum((solution[1] for solution in self.solutions)) / len(self.solutions)
        self.pheromones = {city_index: (ACO_RO + ACO_TAU / avg) * pheromone_value for (city_index, pheromone_value) in
                           self.pheromones.items()}
        self.solutions.sort(key=lambda x: x[1])
        if self.best_solution is not None:
            if self.solutions[0][1] < self.best_solution[1]:
                self.best_solution = self.solutions[0]
            for path in self.best_solution[0]:
                for i in range(len(path) - 1):
                    self.pheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))] += ACO_SIGMA / \
                                                                                               self.best_solution[1]
        else:
            self.best_solution = self.solutions[0]
        for elite_ant in range(ACO_SIGMA):
            paths = self.solutions[elite_ant][0]
            current_cost = self.solutions[elite_ant][1]
            for path in paths:
                for i in range(len(path) - 1):
                    self.pheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))] = (ACO_SIGMA - (
                            elite_ant + 1) / current_cost ** (
                                                                                                       elite_ant + 1)) + \
                                                                                              self.pheromones[(
                                                                                                  min(path[i],
                                                                                                      path[i + 1]),
                                                                                                  max(path[i],
                                                                                                      path[i + 1]))]
        return self.best_solution

    # print solution by the requested format
    def print_solution(self):
        print(f"Cost : {int(self.best_solution[1])}")
        for truck in self.best_solution[0]:
            print(f"Truck{self.best_solution[0].index(truck) + 1}: 1", end=',')
            for city_index in truck:
                print(city_index, end=',')
            print('1')

    # run the algorithm
    def run(self):
        last_best = None
        stuck_counter = 0
        start_time = time.time()
        for i in range(self.max_iter):
            self.solutions = list()
            for _ in range(self.number_of_ants):
                solution = self.find_solution()
                self.solutions.append((solution, self.calc_solution_cost(solution, self.edges)))
            self.best_solution = self.update_pheromone()
            self.print_solution()
            if last_best is None:
                last_best = self.best_solution[1]
            if last_best == self.best_solution[1]:
                stuck_counter += 1
            else:
                last_best = self.best_solution[1]
                stuck_counter = 0
            if (stuck_counter/self.max_iter) >= STUCK_PCT:
                break
            self.iterations_cost.append(int(self.best_solution[1]))
        self.elapsed_time = round(time.time() - start_time, 2)
        self.clock_ticks = self.elapsed_time * CLOCK_RATE
        print(f"Time elapsed {self.elapsed_time}")
        return self.best_solution
