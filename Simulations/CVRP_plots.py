import matplotlib.pyplot as plt


def fill_list_with_last_value(lst: list, max_size: int):
    value = lst[-1]
    while len(lst) < max_size:
        lst.append(value)


if __name__ == '__main__':

    ga_results = {
        1: [379, 385, 383, 375],
        2: [894, 876, 885, 868],
        3: [782, 582, 606, 583],
        4: [1303, 853, 849, 856],
        5: [1362, 959, 946, 957],
        6: [1768, 1237, 1001, 952],
        7: [2046, 1523, 1301, 1190]
    }
    ts_results = {
        1: [393, 392, 389, 381],
        2: [882, 867, 873, 873],
        3: [594, 603, 595, 631],
        4: [826, 847, 804, 801],
        5: [905, 884, 891, 904],
        6: [996, 943, 979, 965],
        7: [1208, 1160, 1166, 1171]
    }
    sa_results = {
        1: [395, 390, 387, 377],
        2: [878, 868, 869, 872],
        3: [642, 601, 583, 532],
        4: [842, 806, 783, 794],
        5: [946, 876, 869, 869],
        6: [1013, 962, 946, 940],
        7: [1215, 1176, 1177, 1161]
    }
    aco_results = {
        1: [380, 378, 380, 378],
        2: [864, 870, 856, 858],
        3: [614, 595, 591, 584],
        4: [817, 851, 847, 845],
        5: [967, 944, 939, 951],
        6: [1015, 961, 975, 964],
        7: [1293, 1281, 1266, 1272]
    }
    iterations = [100, 500, 750, 1000]
    problems = {
        1: "E-n22-k4.txt",
        2: "E-n33-k4.txt",
        3: "E-n51-k5.txt",
        4: "E-n76-k8.txt",
        5: "n76-k10.txt",
        6: "E-n101-k8.txt",
        7: "E-n101-k14.txt"
    }
    for i in range(7):
        current = i + 1
        plt.plot(iterations, ts_results[current])
        plt.plot(iterations, ga_results[current])
        plt.plot(iterations, aco_results[current])
        plt.plot(iterations, sa_results[current])
        plt.legend(["TS", "GA", "ACO", "SA"])
        plt.xlabel("Number Of Iterations")
        plt.ylabel("Cost")
        plt.title(f"Impact of iterations number: {problems[current]}")
        plt.show()
