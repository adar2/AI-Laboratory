from Algorithms.DiscreteOptimizationSearch.LeastDiscrepancySearch import LeastDiscrepancySearch
from Algorithms.LocalSearch.UtilFunctions import euc_distance
from Problems.CVRP import CVRP
from Problems.CVRPSearchProblem import CVRPSearchProblem
from Utils.CVRPFileParsing import parse_cvrp_file
from Utils.Constants import DEMAND, COORDINATES


class CVRPTwoStepSolver:
    def __init__(self, cvrp_problem: CVRPSearchProblem):
        self.problem = cvrp_problem
        self.trucks = []
        self.distance_matrix = []
        self.init_distance_matrix()

    def init_distance_matrix(self):
        for first_location in self.problem.locations:
            distance_vector = []
            for second_location in self.problem.locations:
                if first_location is second_location:
                    distance_vector.append(0)
                    continue
                distance = euc_distance(first_location[COORDINATES], second_location[COORDINATES])
                distance_vector.append(distance)
            self.distance_matrix.append(distance_vector)

    def cost(self, route):
        total_distance = self.distance_matrix[0][route[0]]
        for i in range(len(route) - 1):
            total_distance += self.distance_matrix[route[i]][route[i + 1]]
        total_distance += self.distance_matrix[0][route[-1]]

        return int(total_distance)

    def two_opt(self, route):
        best = route
        improved = True
        while improved:
            improved = False
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route)):
                    if j - i == 1:
                        continue
                    new_route = route[:]
                    new_route[i:j] = route[j - 1:i - 1:-1]
                    if self.cost(new_route) < self.cost(best):
                        best = new_route
                        improved = True
            route = best
        return best

    def solve(self):
        total_distance = 0
        init_config = self.problem.get_initial_config()
        while len(init_config) > 0:
            lds_algo = LeastDiscrepancySearch(self.problem)
            current_truck = lds_algo.run()
            current_truck = self.problem.update_remaining_locations(current_truck)
            self.trucks.append(current_truck)
            init_config = self.problem.get_initial_config()
        for truck_route in self.trucks:
            improved_cost = self.cost(self.two_opt(truck_route))
            total_distance += improved_cost
        print(f'Total cost : {total_distance} , number of trucks : {len(self.trucks)}')


if __name__ == '__main__':
    capacity, locations = parse_cvrp_file('E-n22-k4.txt')
    problem = CVRP(capacity, locations)
    problem1 = CVRPSearchProblem(problem)
    algo = CVRPTwoStepSolver(problem1)
    algo.solve()
