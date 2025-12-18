import pygame
from constants import *
from pygame_gui.elements import UIButton, UIHorizontalSlider
from pygame_gui import UIManager
import pygame_gui
from maze_solver import MazeSolver
from maze_generator import MazeGenerator

goal = (13, 13)

class App:
    def __init__(self, display):
        self.is_running = True
        self.window = display
        self.explored = []
        self.shortest_path = []
        self.path_delay = 0
        self.path_index = 0
        self.animating = False
        self.animating_shortest = False
        self.found_goal = False
        self.maze_generator = MazeGenerator()
        self.maze = self.maze_generator.maze
        self.solver = MazeSolver(self.maze, start, goal)
        self.generator = self.solver.solve()
        self.manager = UIManager((WIDTH, HEIGHT))

        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(self.manager.ui_theme.get_colour("dark_bg"))
        self.font = pygame.font.Font("freesansbold.ttf", 16)
        self.text = self.font.render("Maze size : 15x15", True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = ((WIDTH / 7) * 6, 320)
        self.run()

    def run(self):
        clock = pygame.time.Clock()
        time_delta = clock.tick(FPS) / 1000.0

        bfs_button = UIButton(
            relative_rect=pygame.Rect(((WIDTH / 7) * 6, 50), (100, 50)),
            text="BFS",
            manager=self.manager,
        )
        dfs_button = UIButton(
            relative_rect=pygame.Rect(((WIDTH / 7) * 6, 100), (100, 50)),
            text="DFS",
            manager=self.manager,
        )
        astar_button = UIButton(
            relative_rect=pygame.Rect(((WIDTH / 7) * 6, 150), (100, 50)),
            text="A*",
            manager=self.manager,
        )
        generate_maze_btn = UIButton(
            relative_rect=pygame.Rect(((WIDTH / 7) * 6 - 75, 200), (180, 50)),
            text="Generate a new maze",
            manager=self.manager,
        )
        

        slider = UIHorizontalSlider(
            relative_rect=pygame.Rect(((WIDTH / 7) * 6 - 75, 250), (180, 50)),
            start_value=15,
            value_range=(8, 100),
            manager=self.manager,
        )
        
        export_btn = UIButton(
            relative_rect=pygame.Rect(((WIDTH / 7) * 6 - 50, 350), (100, 50)),
            text="Export maze",
            manager=self.manager,
        )

        self.is_running = True

        while self.is_running:

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.is_running = False
                    self.quit()

                if ev.type == pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element == bfs_button:
                        self.reset()
                        self.animating = True
                    elif ev.ui_element == generate_maze_btn:
                        self.maze = self.maze_generator.generate(
                            slider.get_current_value(), slider.get_current_value()
                        )
                        self.reset()
                    elif ev.ui_element == export_btn:
                        self.maze_generator.export_maze()
                        
                if ev.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if ev.ui_element == slider:
                        self.text = self.font.render(
                            f"Maze size : {ev.value}x{ev.value}", True, (255, 255, 255)
                        )

                self.manager.process_events(ev)

            if self.animating:
                try:
                    cell, path, is_goal = next(self.generator)
                    self.explored.append(cell)

                    if is_goal:
                        self.shortest_path = path
                        self.found_goal = True
                        self.animating = False
                        self.animating_shortest = True
                        self.path_delay = 15
                        self.path_index = 0
                except StopIteration:
                    self.animating = False

            elif self.found_goal and self.path_delay > 0:
                self.path_delay -= 1
                if self.path_delay == 0:
                    self.animating_shortest = True

            elif self.animating_shortest and self.path_index < len(self.shortest_path):
                self.path_index += 1

            self.manager.update(time_delta)
            self.window.blit(self.background, (0, 0))
            self.window.blit(self.text, self.textRect)
            self.manager.draw_ui(self.window)
            self.draw_maze()
            self.draw_explored()
            self.draw_path()
            clock.tick(FPS)
            pygame.display.flip()

    def draw_maze(self):
        for r in range(len(self.maze)):
            for c in range(len(self.maze[r])):
                x = c * self.maze_generator.CELL_SIZE
                y = r * self.maze_generator.CELL_SIZE

                if (r, c) == goal:
                    pygame.draw.rect(
                        self.window,
                        goal_color,
                        (
                            x,
                            y,
                            self.maze_generator.CELL_SIZE,
                            self.maze_generator.CELL_SIZE,
                        ),
                    )
                elif (r, c) == start:
                    pygame.draw.rect(
                        self.window,
                        start_color,
                        (
                            x,
                            y,
                            self.maze_generator.CELL_SIZE,
                            self.maze_generator.CELL_SIZE,
                        ),
                    )
                elif self.maze[r][c] == 1:
                    pygame.draw.rect(
                        self.window,
                        wall_color,
                        (
                            x,
                            y,
                            self.maze_generator.CELL_SIZE,
                            self.maze_generator.CELL_SIZE,
                        ),
                    )
                    pygame.draw.rect(
                        self.window,
                        border_color,
                        (
                            x,
                            y,
                            self.maze_generator.CELL_SIZE,
                            self.maze_generator.CELL_SIZE,
                        ),
                        border_width,
                    )
                else:
                    pygame.draw.rect(
                        self.window,
                        white,
                        (
                            x,
                            y,
                            self.maze_generator.CELL_SIZE,
                            self.maze_generator.CELL_SIZE,
                        ),
                    )

    def draw_explored(self):
        for r, c in self.explored:
            if (r, c) != start and (r, c) != goal:
                x = c * self.maze_generator.CELL_SIZE
                y = r * self.maze_generator.CELL_SIZE
                pygame.draw.rect(
                    self.window,
                    explored_color,
                    (
                        x,
                        y,
                        self.maze_generator.CELL_SIZE,
                        self.maze_generator.CELL_SIZE,
                    ),
                )

    def draw_path(self):
        for i in range(self.path_index):
            r, c = self.shortest_path[i]
            if (r, c) != start and (r, c) != goal:
                x = c * self.maze_generator.CELL_SIZE
                y = r * self.maze_generator.CELL_SIZE
                pygame.draw.rect(
                    self.window,
                    path_color,
                    (
                        x,
                        y,
                        self.maze_generator.CELL_SIZE,
                        self.maze_generator.CELL_SIZE,
                    ),
                )

    def reset(self):
        self.found_goal = False
        self.animating = False
        self.path_delay = 0
        self.path_index = 0
        self.explored = []
        self.shortest_path = []
        self.solver = MazeSolver(self.maze, start, goal)
        self.generator = self.solver.solve()

    def quit(self):
        pygame.quit()
        quit()
