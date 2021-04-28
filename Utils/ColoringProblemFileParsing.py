def coloring_problem_file_parsing(file_name):
    graph = {}
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if line.startswith('p'):
                vertices = int(line.split(' ')[2])
                edges = int(line.split(' ')[3])
                for i in range(1, vertices + 1):
                    graph[i] = set()
            if line.startswith('e'):
                src_vertex = int(line.split(' ')[1])
                dst_vertex = int(line.split(' ')[2])
                graph[src_vertex].add(dst_vertex)
    return graph, vertices, edges


if __name__ == '__main__':
    coloring_problem_file_parsing('../Algorithms/CSPAlgorithms/le450_5a.col')
