import copy

from Problems.AbstarctSearchProblem import AbstractSearchProblem


class MultiKnapsack(AbstractSearchProblem):
    def __init__(self, capacities_list: list, profits_list: list, weights_dict: dict):
        super().__init__()
        self.weights_dict = weights_dict
        self.profits_list = profits_list
        self.capacities_list = capacities_list
        self.number_of_knapsacks = len(self.capacities_list)
        self.sorted_indices = self.get_sorted_configs()
        self.remaining_capacity_dict = {}  # caching

    # should get list of each knapsack's current weight. Finally, the last item of the list should be a list of all items currently
    # chosen
    def printable_data(self, data: list):
        for knapsack_num in range(self.number_of_knapsacks):
            print(
                f'Knapsack number {knapsack_num}:\nCapacity:{data[knapsack_num]} / {self.profits_list[knapsack_num]}\n')
        print('\n')
        print(f'Items in knapsacks:\n {data[-1]}\n')

    # this should sort all items by density and return a sorted list of items
    def get_sorted_configs(self):
        sorted_config = {key: 0 for key in range(len(self.profits_list))}
        for index in range(len(self.profits_list)):
            value = 0
            for weight_list in self.weights_dict.values():
                current_weight = weight_list[index]
                if current_weight > 0:
                    value += self.profits_list[index] / current_weight
                else:
                    value += self.profits_list[index]
            sorted_config[index] = round(value)

        return sorted(sorted_config, key=lambda x: sorted_config[x], reverse=True)

    # this is tricky: we need to see how to differentiate between items that could be put in the knapsack in the future and items
    # that we already decided not to put. possible solution would be each node holding a dict of who was assigned and who wasn't
    # or maybe use another thing instead of 0 and 1 (for example 2 for items that we decided not to put in)
    def calc_upper_bound(self, config):
        config_copy = copy.copy(config)
        remaining_capacity, remaining_capacity_list = self.calc_remaining_capacity(config_copy)
        item_index = 0
        while item_index < len(config_copy):
            if config_copy[item_index] is None:
                config_copy[item_index] = 1
                remaining_capacity, remaining_capacity_list = self.calc_remaining_capacity(config_copy)
                if remaining_capacity < 0:
                    break
            item_index += 1
        estimation = self.calc_value(config_copy)
        if remaining_capacity < 0:
            real_index = self.sorted_indices[item_index]
            knapsack_index = remaining_capacity_list.index(remaining_capacity)
            config_copy[item_index] = None
            remaining_capacity, remaining_capacity_list = self.calc_remaining_capacity(config_copy)
            knapsack_capacity = remaining_capacity_list[knapsack_index]
            estimation = self.calc_value(config_copy)
            fraction = (knapsack_capacity / self.weights_dict[knapsack_index][real_index]) * self.profits_list[
                real_index]
            estimation += fraction
        return estimation

    # return a blank list of items
    def get_initial_config(self):
        return [None] * len(self.profits_list)

    # also need to figure out if capacity is a number or a list (probably a list)
    def calc_remaining_capacity(self, config):
        immutable_config = tuple(config)
        if immutable_config not in self.remaining_capacity_dict:
            capacities_copy = copy.copy(self.capacities_list)
            for item_index in range(len(config)):
                if config[item_index] is None:
                    break
                elif config[item_index] == 1:
                    real_index = self.sorted_indices[item_index]
                    for j in range(len(capacities_copy)):
                        capacities_copy[j] -= self.weights_dict[j][real_index]
            self.remaining_capacity_dict[immutable_config] = min(capacities_copy), capacities_copy
        return self.remaining_capacity_dict[immutable_config]

    def calc_value(self, config):
        value = 0
        for item_index in range(len(config)):
            if config[item_index] is None:
                break
            if config[item_index] == 1:
                real_index = self.sorted_indices[item_index]
                value += self.profits_list[real_index]
        return value

    def expand(self, config) -> list:
        children = []
        for i in range(len(config)):
            if config[i] is None:
                first = copy.copy(config)
                second = copy.copy(config)
                first[i] = 0
                second[i] = 1
                children.append(second)
                children.append(first)
                break
        return children
