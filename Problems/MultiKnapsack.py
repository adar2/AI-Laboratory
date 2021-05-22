from Problems.AbstractProblem import AbstractProblem


class MultiKnapsack(AbstractProblem):
    def __init__(self, capacities_list: list, weights_list: list, profits_dict: dict):
        super().__init__()
        self.profits_dict = profits_dict
        self.weights_list = weights_list
        self.capacities_list = capacities_list
        self.number_of_knapsacks = len(weights_list)

    # should get list of each knapsack's current weight. Finally, the last item of the list should be a list of all items currently
    # chosen
    def printable_data(self, data: list):
        for knapsack_num in range(self.number_of_knapsacks):
            print(f'Knapsack number {knapsack_num}:\nCapacity:{data[knapsack_num]} / {self.weights_list[knapsack_num]}\n')
        print('\n')
        print(f'Items in knapsacks:\n {data[-1]}\n')

    def get_search_space(self):
        pass
