from AbstractProblem import AbstractProblem


class KnapSack(AbstractProblem):

    def __init__(self, capacity, weights, profits):
        super().__init__()
        # knapsack capacity
        self.capacity = capacity
        # items weights
        self.weights = weights
        # items values
        self.profits = profits

    # given list of 1 and 0, indicating which items chosen, calculate the capacity
    def calc_capacity(self, data: list) -> int:
        total_capacity = 0
        items = self.get_search_space()
        if isinstance(data, list):
            for i in range(len(data)):
                if data[i]:
                    total_capacity += items[i][1]
        return total_capacity

    # given list of 1 and 0, indicating which items chosen, calculate the value
    def calc_knapsack_value(self, data: list) -> int:
        total_profit = 0
        items = self.get_search_space()
        if isinstance(data, list):
            for i in range(len(data)):
                if data[i]:
                    total_profit += items[i][0]
        return total_profit

    # get knapsack capacity
    def get_capacity(self):
        return self.capacity

    # get max possible value of items
    def get_max_value(self):
        return sum(self.profits)

    # returns list of tuples each tuple represents (item value,item weight)
    def get_search_space(self):
        return [(self.profits[i], self.weights[i]) for i in range(len(self.profits))]

    def printable_data(self, data: list):
        return ''.join(f'{c},' for c in data)
