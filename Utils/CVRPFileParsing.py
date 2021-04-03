from os import getcwd,listdir
from string import digits

def parse_cvrp_file(file_path):
    capacity = 0
    locations = 1
    config = {capacity: None, locations: []}
    try:
        with open(file_path, 'r') as f:
            for line in  f.readlines():
                if "CAPACITY" in line:
                    config[capacity] = int(line.split(':')[1])
                elif line.startswith(a for a in digits):
                    print(line)

    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    parse_cvrp_file(getcwd() + '\E-n22-k4.txt')

