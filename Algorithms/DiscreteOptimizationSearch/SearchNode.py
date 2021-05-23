class SearchNode:
    def __init__(self, config, upper_bound, capacity, value, discrepancy=0,item_to_expand=0):
        self.item_to_expand = item_to_expand
        self.is_expanded = False
        self.discrepancy = discrepancy
        self.capacity = capacity
        self.upper_bound = upper_bound
        self.config = config
        self.value = value
