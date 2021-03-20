from AbstractProblem import AbstractProblem


class KnapSack(AbstractProblem):

    def __init__(self, capacity, weights, profits):
        super().__init__()
        self.capacity = capacity
        self.weights = weights
        self.profits = profits

    def calc_capacity(self, data: list) -> int:
        total_capacity = 0
        items = self.get_search_space()
        if isinstance(data, list):
            for i in range(len(data)):
                if data[i]:
                    total_capacity += items[i][1]
        return total_capacity

    def calc_knapsack_value(self, data: list) -> int:
        total_profit = 0
        items = self.get_search_space()
        if isinstance(data, list):
            for i in range(len(data)):
                if data[i]:
                    total_profit += items[i][0]
        return total_profit

    def get_capacity(self):
        return self.capacity

    def get_max_value(self):
        return sum(self.profits)

    def get_search_space(self):
        return [(self.profits[i], self.weights[i]) for i in range(len(self.profits))]
