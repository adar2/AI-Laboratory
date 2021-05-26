class SearchNode:
    def __init__(self, config, capacity, value ,upper_bound = 0):
        self.is_expanded = False
        self.capacity = capacity
        self.config = config
        self.value = value
        self.upper_bound = upper_bound
