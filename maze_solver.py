from collections import deque

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
            
            if (row, col) == self.goal:
                yield (row, col), path, True
                return
            
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < len(self.maze) and 
                    0 <= new_col < len(self.maze[0]) and
                    self.maze[new_row][new_col] == 0 and
                    (new_row, new_col) not in visited):
                    
                    visited.add((new_row, new_col))
                    queue.append(((new_row, new_col), path + [(new_row, new_col)]))
    
    def a_star(self):
        pass
    
    def solve(self):
        if self.algorithm == "BFS" :
            return self.bfs()
        elif self.algorithm == "A*":
            return self.a_star()