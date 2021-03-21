import random, time


class MinConflictAlgorithm:
    """
        the number i represents queen number i which stands on column i, the position in the list represents the row of the queen
    """

    def __init__(self, size, max_iter):
        # size of the board and number of queens
        self.size = size
        # maximum iterations to run
        self.max_iter = max_iter
        # iterations counter
        self.iterations = 0
        # time elapsed for the algorithm to terminate
        self.time_elapsed = time.time()
        # did we solve the problem or not
        self.solved = False
        # list which represents the game board , initialized with numbers [0 to size -1]
        self.game_board = [i for i in range(self.size)]
        # shuffle the game board inorder to start from random arrangement
        random.shuffle(self.game_board)

    # check if no conflicts found return true , false otherwise
    def check_goal_state(self) -> bool:
        for i in self.game_board:
            for j in self.game_board:
                if i is j:
                    continue
                if abs(i - j) == abs(self.game_board.index(i) - self.game_board.index(j)):
                    return False
        return True

    # given an index of the game board list,  finds other index which swapping between those minimize the number of
    # conflicts
    def minimize_conflict(self, conflicted_index, conflict_size):
        # min number of conflicts
        min_conflicts = float('inf')
        # index which swapping with leads to minimal number of conflicts
        minimize_index = None
        # iterate through all indexes of the game board
        for i in self.game_board:
            if i == conflicted_index:
                continue
            # swap i and index inorder to check number of conflicts
            self.game_board[conflicted_index], self.game_board[i] = self.game_board[i], self.game_board[
                conflicted_index]
            # count how many conflicts there is after the swap
            total_conflicts = 0
            for j in self.game_board:
                for k in self.game_board:
                    if j == k:
                        continue
                    if abs(k - j) == abs(self.game_board.index(k) - self.game_board.index(j)):
                        total_conflicts += 1
            # if the number of conflicts is less then the min conflicts so far than save the number of conflicts and
            # the swap caused it
            if total_conflicts < min_conflicts:
                min_conflicts = total_conflicts
                minimize_index = i
            # undo the swap
            self.game_board[conflicted_index], self.game_board[i] = self.game_board[i], self.game_board[
                conflicted_index]
        # if the min number of conflicts that was achieved is less then the current conflicts size, do the swap
        if min_conflicts <= conflict_size:
            self.game_board[conflicted_index], self.game_board[minimize_index] = self.game_board[minimize_index], \
                                                                                 self.game_board[conflicted_index]

    def run(self):
        # conflicted pieces list
        conflicted = []
        # iterate until max iterations reached
        for self.iterations in range(self.max_iter):
            # if we have no conflicts were done
            if self.check_goal_state():
                self.solved = True
                self.time_elapsed = time.time() - self.time_elapsed
                print(f"Solution Found : {self.game_board}")
                return
            # total number of conflicts in the current game board
            total_conflicts = 0
            for i in self.game_board:
                # number of conflicts current index is participating
                current_index_conflicts = 0
                for j in self.game_board:
                    if i == j:
                        continue
                    if abs(i - j) == abs(self.game_board.index(i) - self.game_board.index(j)):
                        current_index_conflicts += 1
                total_conflicts += current_index_conflicts
                if current_index_conflicts > 0:
                    # insert piece to conflicted list
                    conflicted.append(i)
            print(f"Current Game Board : {self.game_board} , Number of conflicts : {total_conflicts}")
            if conflicted:
                # choose element from the conflicted list
                random_conflict = random.choice(conflicted)
                # try to swap between elements to minimize current conflicts
                self.minimize_conflict(random_conflict, total_conflicts)
                conflicted.clear()
        self.time_elapsed = time.time() - self.time_elapsed

