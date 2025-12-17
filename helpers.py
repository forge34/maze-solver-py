import random

def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    stack = [(1, 1)]
    maze[1][1] = 0
    directions = [(0,2),(2,0),(0,-2),(-2,0)]

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        carved = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < rows-1 and 0 < ny < cols-1 and maze[nx][ny] == 1:
                maze[x + dx//2][y + dy//2] = 0
                maze[nx][ny] = 0
                stack.append((nx, ny))
                carved = True
                break

        if not carved:
            stack.pop()

    maze[0][1] = 0
    maze[rows-1][cols-2] = 0
    return maze

def manhattan_distance(point, goal):
    x1, y1 = point
    x2, y2 = goal
    return abs(x2 - x1) + abs(y2 - y1)

def maze_heuristic(maze, goal):
    return [
        [manhattan_distance((c, r), goal) for c in range(len(maze[r]))]
        for r in range(len(maze))
    ]

            