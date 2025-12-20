from constants import HEIGHT
from helpers import generate_maze
from datetime import datetime
import os
import random
import math

default_maze = [
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
]


class MazeGenerator:
    def __init__(self, maze=default_maze):
        self.maze = maze
        self.maze_rows = len(self.maze)
        self.maze_cols = len(self.maze[0])

        self.maze_width = HEIGHT - 25
        self.maze_height = HEIGHT - 25
        self.CELL_SIZE = min(
            math.ceil(self.maze_width / self.maze_cols),
            math.ceil(self.maze_height / self.maze_rows),
        )

    def generate(self, rows, cols):
        self.maze = generate_maze(rows, cols)
        self.add_loops(self.maze)
        self.update_props()
        return self.maze

    def update_props(self):
        self.maze_rows = len(self.maze)
        self.maze_cols = len(self.maze[0])
        self.CELL_SIZE = min(
            math.ceil(self.maze_width / self.maze_cols),
            math.ceil(self.maze_height / self.maze_rows),
        )

    def export_maze(self,goal):
        os.makedirs("mazes", exist_ok=True)

        filename = f"maze_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join("mazes", filename)

        with open(path, "w") as f:
            f.write(str(self.maze))
            f.write(f"Goal : ({goal[0]},{goal[1]})")

    def add_loops(self, maze, chance=0.15):
        rows, cols = len(maze), len(maze[0])
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if maze[i][j] == 1 and random.random() < chance:
                    if maze[i - 1][j] == 0 and maze[i + 1][j] == 0:
                        maze[i][j] = 0
                    elif maze[i][j - 1] == 0 and maze[i][j + 1] == 0:
                        maze[i][j] = 0
