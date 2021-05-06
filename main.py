import os

from Utils.Config import get_algorithm

if __name__ == '__main__':
    # ***Release Configuration***
    algo = get_algorithm(os.getcwd())
    algo.run()
    input('Please press any key to exit...')
