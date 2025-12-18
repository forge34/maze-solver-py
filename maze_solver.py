from collections import deque

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
        pass
    
    def solve(self):
        if self.algorithm == "BFS" :
            return self.bfs()
        elif self.algorithm == "A*":
            return self.a_star()