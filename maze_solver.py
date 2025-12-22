from collections import deque
from helpers import manhattan_distance
from datetime import datetime
import os
import heapq
import time
import json

def is_wall(grid, row, col):
    return grid[row][col] == 1


def is_valid(grid, row, col):
    return (0 <= row < len(grid)) and (0 <= col < len(grid[0]))


def is_goal(point, goal):
    return point[0] == goal[0] and point[1] == goal[1]


def get_directions():
    return [(0, 1), (1, 0), (0, -1), (-1, 0)]


class MazeSolver:
    def __init__(self, maze, start, goal, algorithm="BFS"):
        self.maze = maze
        self.algorithm = algorithm
        self.explored = []
        self.path = []
        self.start = start
        self.goal = goal
        self.total_time = 0


    def dfs(self):
        visited = {self.start}
        explored = [self.start]
        time_start = time.time()
        stack = [(self.start , [self.start])]
        
        while stack:
            (row,col) ,path = stack.pop()
            
            yield (row,col) ,path , False
            
            if is_goal((row, col), self.goal):
                self.explored = explored
                self.total_time = time.time() - time_start
                self.path = path
                yield (row, col), path, True
                return
            
            for dr, dc in get_directions():
                new_row, new_col = row + dr, col + dc

                if (
                    is_valid(self.maze, new_row, new_col)
                    and not is_wall(self.maze, new_row, new_col)
                    and (new_row, new_col) not in visited
                ):

                    visited.add((new_row, new_col))
                    explored.append((new_row,new_col))
                    stack.append(((new_row, new_col), path + [(new_row, new_col)]))
    def bfs(self):
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        explored = [self.start]
        time_start = time.time()
        while queue:
            (row, col), path = queue.popleft()

            yield (row, col), path, False

            if is_goal((row, col), self.goal):
                self.explored = explored
                self.total_time = time.time() - time_start
                self.path = path
                yield (row, col), path, True
                return

            for dr, dc in get_directions():
                new_row, new_col = row + dr, col + dc

                if (
                    is_valid(self.maze, new_row, new_col)
                    and not is_wall(self.maze, new_row, new_col)
                    and (new_row, new_col) not in visited
                ):

                    visited.add((new_row, new_col))
                    explored.append((new_row,new_col))
                    queue.append(((new_row, new_col), path + [(new_row, new_col)]))

    def a_star(self):
        start_node = (self.start, [self.start])
        priority_queue = [
            (0 + manhattan_distance(self.start, self.goal), 0, start_node)
        ]

        visited = {self.start: 0}
        explored = [self.start]
        time_start = time.time()

        while priority_queue:
            f_score, g_score, (current_pos, path) = heapq.heappop(priority_queue)
            row, col = current_pos

            yield (row, col), path, False

            if g_score > visited.get(current_pos, float("inf")):
                continue

            if is_goal(current_pos, self.goal):
                self.explored = visited
                self.total_time = time.time() - time_start
                self.path = path
                yield (row, col), path, True
                return

            for dr, dc in get_directions():
                new_row, new_col = row + dr, col + dc
                neighbor = (new_row, new_col)
                new_g_score = g_score + 1

                if is_valid(self.maze, new_row, new_col) and not is_wall(
                    self.maze, new_row, new_col
                ):

                    if neighbor not in visited or new_g_score < visited[neighbor]:
                        visited[neighbor] = new_g_score
                        f_score = new_g_score + manhattan_distance(neighbor, self.goal)
                        explored.append((new_row,new_col))

                        new_path = path + [neighbor]
                        heapq.heappush(
                            priority_queue, (f_score, new_g_score, (neighbor, new_path))
                        )

    def export_json(self):
        os.makedirs("json",exist_ok=True)
        size = len(self.maze)
        search_time = float("%0.2f" % (self.total_time))
        explored_count = len(self.explored)
        shortest_count = len(self.path)
        filename = (
            f"{self.algorithm}_{size}x{size}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        content = {
            "algorithm" : self.algorithm,
            "shortest_path_count" : shortest_count,
            "explored_nodes_count" : explored_count,
            "total_time" : search_time,
            "maze" : self.maze,
            "shortest_path" : [list(t) for t in self.path],
            "explored_nodes" : [list(t) for t in self.explored],
            
        }
        
        path = os.path.join("json",filename)
        
        with open(path,"w") as f:
            json.dump(content,f,ensure_ascii=False,indent=4,separators=(",", ": "))
        
    def export_analysis(self):

        os.makedirs("analysis", exist_ok=True)

        size = len(self.maze)
        filename = (
            f"{self.algorithm}_{size}x{size}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        path = os.path.join("analysis", filename)

        maze_str = "\n".join(" ".join(map(str, row)) for row in self.maze)

        explored_str = ", ".join(map(str, self.explored))
        shortest_str = ", ".join(map(str, self.path))

        content = f"""
=== Maze Analysis ===

Algorithm        : {self.algorithm}
Maze size        : {size} x {size}
Explored count   : {len(self.explored)}
Shortest path length : {len(self.path)}
Total time       : {float("%0.2f" % (self.total_time))} Seconds

Maze:
{maze_str}

Explored Nodes:
{explored_str}

Shortest path Nodes:
{shortest_str}
""".strip()

        with open(path, "w") as f:
            f.write(content)

    def solve(self):
        if self.algorithm == "BFS":
            return self.bfs()
        elif self.algorithm == "A*":
            return self.a_star()
        elif self.algorithm == "DFS":
            return self.dfs()
