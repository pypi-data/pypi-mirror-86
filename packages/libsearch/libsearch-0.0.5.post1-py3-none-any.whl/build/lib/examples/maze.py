"""
For function output_image to work and export the solution in a maze drawing in .png 
you should install pillow first in your environment.

pip install pillow

or

pip install -r requirements.txt
"""



import os, sys

class Maze():
    """
    A Maze representation, reads a maze scheme from .txt file and creates Maze object
    source: https://cs50.harvard.edu/ai/2020/
    """

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

    def neighbors_bb(self, action, state): #add action for BB path_cost arguments to work although not required for the maze
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


    def neighbors(self, state):
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

    
    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")


#example of uninformed search

from libsearch import breadth_first_search
## using breadth_first_search and return number of explored states(num_explored) and closed frontier(explored) along with solution
m.solution, m.num_explored, m.explored = breadth_first_search(actions=m.neighbors, start=m.start, goal=m.goal, count_states=True, show_explored=True)
print(50*"*")
print("Solution variable: {}".format(m.solution))
print("Graphic Solution (Breadth first Search):")
m.print()
m.output_image("blind_breadth_fs.png", show_explored=True)

#example for informed search
'''
from libsearch import a_star, best_first_search
## using a_star and return number of explored states(num_explored) and closed frontier(explored) along with solution
m.solution, m.num_explored, m.explored = a_star(actions=m.neighbors, start=m.start, goal=m.goal, heuristic=m.manhattan_distance, count_states=True, show_explored=True)
print(50*"*")
print("Solution variable: {}".format(m.solution))
print("States Explored:", m.num_explored)
print("Graphic Solution (A Star):")
m.print()
m.output_image("informed_a_star.png", show_explored=True)
'''



'''
## using best_first_search and return number of explored states(num_explored) and closed frontier(explored) along with solution
m.solution, m.num_explored, m.explored = best_first_search(actions=m.neighbors, start=m.start, goal=m.goal, heuristic=m.manhattan_distance, count_states=True, show_explored=True)
print(50*"*")
print("Solution variable: {}".format(m.solution))
print("States Explored:", m.num_explored)
print("Graphic Solution (Best First Search):")
m.print()
m.output_image("informed_best_fs.png", show_explored=True)
'''
