import pygame
from constants import *

white = [255, 255, 255]
background = [125, 125, 125]
black = (0, 0, 0)
goal_color = (0, 255, 0)
start_color = (0, 0, 255)


maze = [
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

CELL_SIZE = 30

maze_width = len(maze[0]) * CELL_SIZE
maze_height = len(maze) * CELL_SIZE

x_offset = 0 #(WIDTH - maze_width) // 2
y_offset = 0 #(HEIGHT - maze_height) // 2


class App:
    def __init__(self, display):
        self.is_running = True
        self.window = display

        self.run()

    def run(self):
        clock = pygame.time.Clock()

        self.is_running = True
        self.window.fill(background)

        self.draw_maze()
        pygame.display.flip()
        
        STEPS_PER_FRAME = 1

        while self.is_running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.is_running = False
                    self.quit()

        clock.tick()

    def draw_maze(self):
        for r in range(len(maze)):
            for c in range(len(maze[r])):
                x = c * CELL_SIZE + x_offset
                y = r * CELL_SIZE + y_offset

                if (r, c) == goal:
                    pygame.draw.rect(
                        self.window, goal_color, (x, y, CELL_SIZE, CELL_SIZE)
                    )
                elif (r, c) == start:
                    pygame.draw.rect(
                        self.window, start_color, (x, y, CELL_SIZE, CELL_SIZE)
                    )
                elif maze[r][c] == 1:
                    pygame.draw.rect(self.window, wall_color, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(
                    self.window,
                    border_color,
                    (x, y, CELL_SIZE, CELL_SIZE),
                    border_width,
                )
                else:
                    pygame.draw.rect(self.window, white, (x, y, CELL_SIZE, CELL_SIZE))                

        
    def quit(self):
        pygame.quit()
        quit()
