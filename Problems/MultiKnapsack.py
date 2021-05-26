import copy

from Problems.AbstarctSearchProblem import AbstractSearchProblem


class MultiKnapsack(AbstractSearchProblem):
    def __init__(self, capacities_list: list, weights_list: list, profits_dict: dict):
        super().__init__()
        self.profits_dict = profits_dict
        self.weights_list = weights_list
        self.capacities_list = capacities_list
        self.number_of_knapsacks = len(self.capacities_list)

    # should get list of each knapsack's current weight. Finally, the last item of the list should be a list of all items currently
    # chosen
    def printable_data(self, data: list):
        for knapsack_num in range(self.number_of_knapsacks):
            print(
                f'Knapsack number {knapsack_num}:\nCapacity:{data[knapsack_num]} / {self.weights_list[knapsack_num]}\n')
        print('\n')
        print(f'Items in knapsacks:\n {data[-1]}\n')

    # this should sort all items by density and return a sorted list of items
    def get_sorted_configs(self):
        pass

    # this is tricky: we need to see how to differentiate between items that could be put in the knapsack in the future and items
    # that we already decided not to put. possible solution would be each node holding a dict of who was assigned and who wasn't
    # or maybe use another thing instead of 0 and 1 (for example 2 for items that we decided not to put in)
    def calc_upper_bound(self, config):
        raise NotImplementedError

    # return a blank list of items
    def get_initial_config(self):
        return [None] * len(self.weights_list)

    # also need to figure out if capacity is a number or a list (probably a list)
    def calc_remaining_capacity(self, config):
        capacities_copy = copy.copy(self.capacities_list)
        for i in range(len(config)):
            if config[i] is  None:
                break
            elif config[i] == 1:
                for j in range(len(capacities_copy)):
                    # capacities_copy[j] -= self.weights_list[i]
                    capacities_copy[j] -= self.profits_dict[j][i]
        return min(capacities_copy)

    def calc_value(self, config):
        value = 0
        for item_index in range(len(config)):
            if config[item_index] == 1:
                # profits dict should return a list of the current item's profits in each knapsack
                for knapsack_profits in self.profits_dict.values():
                    # add up the profits to account for all knapsacks (initial thought, might not be what we want)
                    value += knapsack_profits[item_index]
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
