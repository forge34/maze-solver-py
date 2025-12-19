from collections import deque
from helpers import manhattan_distance
import heapq

def is_wall(grid,row,col):
    return grid[row][col] == 1

def is_valid(grid,row,col):
    return (0 <= row < len(grid)) and (0 <= col < len(grid[0]))

def is_goal(point,goal):
    return point[0] == goal[0] and point[1] == goal[1]

def get_directions():
    return [(0, 1), (1, 0), (0, -1), (-1, 0)]

class MazeSolver:
    def __init__(self,maze,start,goal,algorithm = "BFS"):
        self.maze = maze
        self.algorithm = algorithm
        self.explored = []
        self.path = []
        self.start = start
        self.goal = goal
        pass
    
    def bfs(self):
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        
        while queue:
            (row, col), path = queue.popleft()
            
            yield (row, col), path, False
            
            if is_goal((row,col) , self.goal):
                yield (row, col), path, True
                return
            
            for dr, dc in get_directions():
                new_row, new_col = row + dr, col + dc
                
                if (is_valid(self.maze , new_row,new_col) and
                    not is_wall(self.maze ,new_row,new_col) and
                    (new_row, new_col) not in visited):
                    
                    visited.add((new_row, new_col))
                    queue.append(((new_row, new_col), path + [(new_row, new_col)]))
    
    def a_star(self):
        start_node = (self.start, [self.start])
        priority_queue = [(0 + manhattan_distance(self.start, self.goal), 0, start_node)]
        
        visited = {self.start: 0}
        
        while priority_queue:
            f_score, g_score, (current_pos, path) = heapq.heappop(priority_queue)
            row, col = current_pos
            
            yield (row, col), path, False
            
            if g_score > visited.get(current_pos, float('inf')):
                continue
            
            if is_goal(current_pos, self.goal):
                yield (row, col), path, True
                return
            
            for dr, dc in get_directions():
                new_row, new_col = row + dr, col + dc
                neighbor = (new_row, new_col)
                new_g_score = g_score + 1 
                
                if (is_valid(self.maze, new_row, new_col) and 
                    not is_wall(self.maze, new_row, new_col)):
                    
                    if neighbor not in visited or new_g_score < visited[neighbor]:
                        visited[neighbor] = new_g_score
                        f_score = new_g_score + manhattan_distance(neighbor, self.goal)
                        
                        new_path = path + [neighbor]
                        heapq.heappush(priority_queue, (f_score, new_g_score, (neighbor, new_path)))
        
    
    def solve(self):
        if self.algorithm == "BFS" :
            return self.bfs()
        elif self.algorithm == "A*":
            return self.a_star()