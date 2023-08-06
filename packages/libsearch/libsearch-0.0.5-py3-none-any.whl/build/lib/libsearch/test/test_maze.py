"""
A Maze representation to test implemented search algorithms
"""


import os, sys
import pytest
class Maze():

    def __init__(self, filename):
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        my_data_path = os.path.join(THIS_DIR, filename)
        # Read file and set height and width of maze
        with open(my_data_path) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state): #add action for BB path_cost arguments to work although not required for the maze
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def manhattan_distance(self, a, b):
        distance = abs(a[0]-b[0]) + abs(a[1] - b[1])
        print("MAnhatan distance: {}".format(distance))
        return distance

    def path_cost(self, a, b):
        """
        the cost of moving to a new tile is always 1
        this function is used in case a path cost is required as input for an algorithm (ex. Branch and Bound)
        """
        return 1


#test for general solution uninformed search
m = Maze("maze4.txt")

from libsearch import depth_first_search, breadth_first_search, iterative_deepening
def test_depth_first_search():
    assert depth_first_search(actions=m.neighbors, start=m.start, goal=m.goal) == (['right', 'right', 'right', 'up', 'up', 'left', 'left', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'], [(6, 1), (6, 2), (6, 3), (5, 3), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11)])
def test_breadth_first_search():
    assert breadth_first_search(actions=m.neighbors, start=m.start, goal=m.goal) == (['right', 'right', 'right', 'up', 'up', 'left', 'left', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'], [(6, 1), (6, 2), (6, 3), (5, 3), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11)])
def test_iterative_deepening():
    assert iterative_deepening(actions=m.neighbors, start=m.start, goal=m.goal) == (['right', 'right', 'right', 'up', 'up', 'left', 'left', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'], [(6, 1), (6, 2), (6, 3), (5, 3), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11)])


#test for general solution informed search
m2 = Maze("maze4.txt")
from libsearch import a_star,best_first_search ,iterative_deepening_a_star
def test_a_star():
    assert a_star(actions=m2.neighbors, start=m2.start, goal=m2.goal, heuristic=m2.manhattan_distance) == (['right', 'right', 'right', 'up', 'up', 'left', 'left', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'], [(6, 1), (6, 2), (6, 3), (5, 3), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11)])
def test_best_first_search():
    assert best_first_search(actions=m2.neighbors, start=m2.start, goal=m2.goal, heuristic=m2.manhattan_distance) == (['right', 'right', 'right', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'down', 'down', 'left', 'left', 'left', 'left', 'down', 'down', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up'], [(6, 1), (6, 2), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 9), (4, 9), (4, 8), (4, 7), (4, 6), (4, 5), (5, 5), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (5, 11), (4, 11), (3, 11), (2, 11), (1, 11), (0, 11)])
def test_iterative_deepening_a_star():
    assert iterative_deepening_a_star(actions=m2.neighbors, start=m2.start, goal=m2.goal, heuristic=m2.manhattan_distance) == (['right', 'right', 'right', 'up', 'up', 'left', 'left', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'], [(6, 1), (6, 2), (6, 3), (5, 3), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11)])
#print("States Explored:", m.num_explored)
#print("Solution:")
#m.print()
