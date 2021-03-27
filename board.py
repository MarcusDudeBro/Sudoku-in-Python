from tree import Tree
from random import random, randint
from copy import deepcopy


class Gameboard:
    def __init__(self):
        self.solution = []
        self.og_board = []
        self.board = [[0]*9 for i in range(9)]
        self.empty_spaces = 0
        self.rect = None

    def remove_candidates(self, candidates, number):
        try:
            candidates.remove(number)
        except ValueError:
            pass

    def create_solution(self):
        tree = Tree()
        for row in range(9):
            previous = tree.add_root(None)
            col = 0
            while col < 9:
                if tree.children(previous) is None:
                    candidates = [i for i in range(1, 10)]
                    for i in range(0, col):
                        self.remove_candidates(candidates, self.board[row][i])
                    for i in range(0, row):
                        self.remove_candidates(candidates, self.board[i][col])
                    for i in range(row//3 * 3, row):
                        for j in range(col//3 * 3, col//3 * 3 + 3):
                            self.remove_candidates(candidates, self.board[i][j])
                    tree.add_children(previous, candidates)
                if len(tree.children(previous)) == 0:
                    tree.remove(previous)
                    previous = tree.parent(previous)
                    col -= 1
                    self.board[row][col] = 0
                else:
                    children = tree.children(previous)
                    previous = children[randint(0, len(children)-1)]
                    self.board[row][col] = previous.get_element()
                    col += 1
        self.solution = deepcopy(self.board)
        for row in range(9):
            for col in range(9):
                if random() <= 0.64:
                    self.board[row][col] = 0
                    self.empty_spaces += 1
        self.og_board = deepcopy(self.board)

    def check(self):
        """ checks if there are any errors on a gameboard
        return(errors): returns true if there are errors and false otherwise
        """
        errors = []
        # check horizontals
        for i in range(9):
            number_pos = [[] for k in range(9)]
            for j in range(9):
                if self.board[i][j] != 0:
                    number_pos[self.board[i][j]-1].append((j, i))
            for positions in number_pos:
                if len(positions) > 1:
                    for pos in positions:
                        errors.append(pos)
            # check verticals
            number_pos = [[] for k in range(9)]
            for j in range(9):
                if self.board[j][i] != 0:
                    number_pos[self.board[j][i]-1].append((i, j))
            for positions in number_pos:
                if len(positions) > 1:
                    for pos in positions:
                        errors.append(pos)
            # check boxes
            number_pos = [[] for k in range(9)]
            for row in range(i//3 * 3, i//3 * 3 + 3):
                for col in range(i % 3 * 3, i % 3 * 3 + 3):
                    if self.board[row][col] != 0:
                        number_pos[self.board[row][col]-1].append((col, row))
            for positions in number_pos:
                if len(positions) > 1:
                    for pos in positions:
                        errors.append(pos)
        return errors

    def solve(self):
        self.board = deepcopy(self.solution)

    def clear(self):
        self.board = deepcopy(self.og_board)
