def parse_cvrp_file(file_path):
    capacity = 0
    locations = 1
    config = {capacity: None, locations: []}
    coords = []
    demands = []
    demand_flag = False
    try:
        with open(file_path, 'r') as f:
            data = f.readlines()
            for line in data:
                if "DIMENSION" in line:
                    size = int(line.split(':')[1])
                elif "CAPACITY" in line:
                    config[capacity] = int(line.split(':')[1])
                elif line[0].isdigit():
                    if not demand_flag:
                        coords.append((int(line.split(' ')[1]), int(line.split(' ')[2])))
                    else:
                        demands.append(int(line.split(' ')[1]))
                elif "DEMAND_SECTION" in line:
                    demand_flag = True
                elif "DEPOT_SECTION" in line:
                    break

    except FileNotFoundError as e:
        print(e)
    for coord in coords:
        config[locations].append((coord, demands[coords.index(coord)]))
    return config[capacity], config[locations]

