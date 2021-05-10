from Utils.ColoringProblemFileParsing import coloring_problem_file_parsing
from Problems.GraphColoringProblem import GraphColoringProblem
from Algorithms.CSPAlgorithms.BackJumpingAlgorithm import BackJumpingAlgorithm
from Algorithms.CSPAlgorithms.ForwardCheckingAlgorithm import ForwardCheckingAlgorithm
from Algorithms.LocalSearch.ColoringTabuSearch import ColoringTabuSearch
from Algorithms.LocalSearch.KempeChainsAlgorithm import KempeChainsAlgorithm
from Algorithms.LocalSearch.HybridColoringAlgorithm import HybridColoringAlgorithm
from Algorithms.GeneticAlgorithm.ColoringGeneticAlgorithm import ColoringGeneticAlgorithm
import xlwt

if __name__ == '__main__':
    test_files = ['games120.col', 'le450_15a.col','huck.col','jean.col','le450_5b.col']
    max_iter = 5000
    # results_file = open("CSP Simulations.txt",'a')
    workbook = xlwt.Workbook()
    for file in test_files:
        sheet = workbook.add_sheet(file)
        sheet.write(0,0,"Algorithm")
        sheet.write(0,1,"Chromatic Number")
        sheet.write(0,2,"States Explored")
        sheet.write(0,3,"Runtime")
        graph, vertices, edges = coloring_problem_file_parsing(file)
        problem = GraphColoringProblem(graph, vertices, edges)
        # results_file.write('------------------------------------------')
        # results_file.write(f'Results of {file}:\n')
        backjumping = BackJumpingAlgorithm(problem)
        forward_checking = ForwardCheckingAlgorithm(problem)
        tabu = ColoringTabuSearch(problem, max_iter)
        kempe = KempeChainsAlgorithm(problem,max_iter)
        hybrid = HybridColoringAlgorithm(problem,max_iter)
        ga = ColoringGeneticAlgorithm(200,max_iter,problem)
        algorithms = [backjumping,forward_checking,tabu,kempe,hybrid,ga]
        line = 1
        for algorithm in algorithms:
            # results_file.write(f'{algorithm.__class__.__name__}:\n')
            # results_file.write(f'Solution: {algorithm.run()}\n')
            # results_file.write(f'States Explored: {algorithm.states_explored}\n')
            # results_file.write(f'Run Time: {algorithm.elapsed_time}\n')
            sheet.write(line,0,algorithm.__class__.__name__)
            sheet.write(line,1,algorithm.run())
            sheet.write(line,2,algorithm.states_explored)
            sheet.write(line,3,algorithm.elapsed_time)
            line += 1
    # results_file.close()
    workbook.save('CSP_summary.xls')


