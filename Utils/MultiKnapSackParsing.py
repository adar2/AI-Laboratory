def multiknapsack_problem_file_parsing(file_name):
    profits_dict = {}
    capacities = []
    weights = []
    index = 2
    with open(file_name, 'r') as f:
        data = f.read().split()
        num_of_knapsacks = int(data[0])
        num_of_objects = int(data[1])

        limit = num_of_objects + index
        while index < limit:
            weights.append(int(data[index]))
            index += 1

        limit = num_of_knapsacks + index
        while index < limit:
            capacities.append(int(data[index]))
            index += 1

        for i in range(num_of_knapsacks):
            profits_dict[i] = []
            for _ in range(num_of_objects):
                profits_dict[i].append(data[index])
                index += 1

        return profits_dict, capacities, weights
