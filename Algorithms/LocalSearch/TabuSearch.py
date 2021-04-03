from Algorithms.LocalSearch.BaseIterativeLocalSearch import BaseIterativeLocalSearch
from Problems.AbstractProblem import AbstractProblem
from Algorithms.LocalSearch.TabuList import TabuList
from Algorithms.LocalSearch.Neighborhood import random_move_neighborhood as get_neighborhood
from Utils.Constants import INITIAL_TABU_TENURE, COORDINATES, DEMAND


class TabuSearch(BaseIterativeLocalSearch):
    def __init__(self, problem: AbstractProblem, max_iter: int):
        super().__init__(problem, max_iter)
        self.tabu_list = None

    def __convert_to_key(self, config):
        # convert to tuple of (x,y,demand)
        hash_key = []
        for location in config:
            hash_key.append(self.cities_dict[location[COORDINATES]])
        return tuple(hash_key)


    def run(self):
        self.current_config = self.init_config()
        self.current_config_cost = self.cost(self.current_config)
        self.tabu_list = TabuList(len(self.current_config) / 10, INITIAL_TABU_TENURE)
        self.best_config = self.current_config
        self.best_config_cost = self.cost(self.best_config)
        for i in range(self.max_iter):
            print(f"best config : {self.best_config} , cost: {self.best_config_cost}")
            self.proposed_config = self.neighbour_config()
            proposed_config_cost = self.cost(self.proposed_config)
            previous_config_cost = self.current_config_cost
            self.current_config = self.proposed_config
            improvement_delta = previous_config_cost - proposed_config_cost
            self.current_config_cost = self.cost(self.proposed_config)
            if self.current_config_cost < self.best_config_cost:
                self.best_config = self.current_config
                self.best_config_cost = self.current_config_cost
            current_config_hash_key = self.__convert_to_key(self.current_config)
            self.tabu_list.add(current_config_hash_key)
            if improvement_delta >= 0:
                self.tabu_list.capacity += 1
            elif abs(improvement_delta) > 0.1 * previous_config_cost:
                self.tabu_list.capacity -= 1
                self.tabu_list.tenure += 1
            self.tabu_list.update()
        print(f'Final Cost: {self.best_config_cost}')
        return self.best_config_cost

    def neighbour_config(self) -> list:
        neighborhood = get_neighborhood(self.current_config)
        min_neighbor = None
        min_neighbor_cost = None
        for neighbor in neighborhood:
            neighbor_cost = self.cost(neighbor)
            neighbor_hash_key = self.__convert_to_key(neighbor)
            if neighbor_hash_key not in self.tabu_list and neighbor_cost < self.current_config_cost:
                if min_neighbor is None:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
                elif neighbor_cost < min_neighbor_cost:
                    min_neighbor = neighbor
                    min_neighbor_cost = neighbor_cost
        return min_neighbor if min_neighbor is not None else self.current_config
