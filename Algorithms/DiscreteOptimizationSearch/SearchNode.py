class SearchNode:
    def __init__(self, config, capacity, value):
        self.is_expanded = False
        self.capacity = capacity
        self.config = config
        self.value = value
