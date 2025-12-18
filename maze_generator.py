from constants import HEIGHT, WIDTH
from helpers import generate_maze
from datetime import datetime
import os
import random

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
        self.CELL_SIZE = min(WIDTH // self.maze_cols, HEIGHT // self.maze_rows)

        self.maze_width = self.maze_cols * self.CELL_SIZE
        self.maze_height = self.maze_rows * self.CELL_SIZE

    def generate(self, rows, cols):
        self.maze = generate_maze(rows, cols)
        self.add_loops(self.maze)
        self.update_props()
        return self.maze

    def update_props(self):
        self.maze_rows = len(self.maze)
        self.maze_cols = len(self.maze[0])
        self.CELL_SIZE = min(WIDTH // self.maze_cols, HEIGHT // self.maze_rows)

        self.maze_width = self.maze_cols * self.CELL_SIZE
        self.maze_height = self.maze_rows * self.CELL_SIZE

    def export_maze(self):
        os.makedirs("mazes", exist_ok=True)

        filename = f"maze_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join("mazes", filename)

        with open(path, "w") as f:
            f.write(str(self.maze))

    def add_loops(self,maze, chance=0.15):
        rows, cols = len(maze), len(maze[0])
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if maze[i][j] == 1 and random.random() < chance:
                    if maze[i - 1][j] == 0 and maze[i + 1][j] == 0:
                        maze[i][j] = 0
                    elif maze[i][j - 1] == 0 and maze[i][j + 1] == 0:
                        maze[i][j] = 0
