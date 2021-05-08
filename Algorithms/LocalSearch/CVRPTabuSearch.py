from Algorithms.LocalSearch.TabuSearch import TabuSearch
from Problems.CVRP import CVRP
from Algorithms.LocalSearch.Neighborhood import random_move_neighborhood as get_neighborhood
from Algorithms.LocalSearch.UtilFunctions import cvrp_path_cost, CVRP_init_config
from Utils.Constants import COORDINATES


class CVRPTabuSearch(TabuSearch):

    def __init__(self, problem: CVRP, max_iter: int):
        super().__init__(problem, max_iter)

    def neighbour_config(self) -> list:
        neighborhood = get_neighborhood(self.current_config)
        min_neighbor = None
        min_neighbor_cost = None
        for neighbor in neighborhood:
            neighbor_cost = self.cost(neighbor)
            neighbor_hash_key = self.convert_to_key(neighbor)
            if neighbor_hash_key not in self.tabu_list and neighbor_cost < self.current_config_cost:
                if min_neighbor is None:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
                elif neighbor_cost < min_neighbor_cost:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
        return min_neighbor if min_neighbor is not None else self.current_config

    def init_config(self):
        return CVRP_init_config(self.problem)

    def cost(self, config) -> float:
        return cvrp_path_cost(self.problem,config)

    def convert_to_key(self, config):
        # convert to tuple of (x,y,demand)
        hash_key = []
        for location in config:
            hash_key.append(self.problem.cities_dict[location[COORDINATES]])
        return tuple(hash_key)


