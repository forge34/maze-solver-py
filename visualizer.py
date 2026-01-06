import heapq
from collections import deque
import graphviz


def get_directions():
    return [(0, 1), (1, 0), (0, -1), (-1, 0)]

def is_valid(maze, r, c):
    return 0 <= r < len(maze) and 0 <= c < len(maze[0])

def is_wall(maze, r, c):
    return maze[r][c] == 1

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(parent_map, start, goal):
    path = []
    curr = goal
    while curr != start:
        path.append(curr)
        if curr not in parent_map: return [] 
        curr = parent_map[curr]
    path.append(start)
    return path[::-1]

def dfs(maze, start, goal):
    start, goal = tuple(start), tuple(goal)
    visited = {start}
    stack = [start]
    parent_map = {}
    
    while stack:
        curr = stack.pop()
        if curr == goal:
            return parent_map, reconstruct_path(parent_map, start, goal)
        
        for dr, dc in get_directions():
            neighbor = (curr[0] + dr, curr[1] + dc)
            if is_valid(maze, neighbor[0], neighbor[1]) and not is_wall(maze, neighbor[0], neighbor[1]) and neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = curr
                stack.append(neighbor)
    return parent_map, []

def bfs(maze, start, goal):
    start, goal = tuple(start), tuple(goal)
    queue = deque([start])
    visited = {start}
    parent_map = {}
    
    while queue:
        curr = queue.popleft()
        if curr == goal:
            return parent_map, reconstruct_path(parent_map, start, goal)
            
        for dr, dc in get_directions():
            neighbor = (curr[0] + dr, curr[1] + dc)
            if is_valid(maze, neighbor[0], neighbor[1]) and not is_wall(maze, neighbor[0], neighbor[1]) and neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = curr
                queue.append(neighbor)
    return parent_map, []

def a_star(maze, start, goal):
    start, goal = tuple(start), tuple(goal)
    pq = [(manhattan_distance(start, goal), 0, start)]
    visited_g = {start: 0}
    parent_map = {}

    while pq:
        f, g, curr = heapq.heappop(pq)
        if curr == goal:
            return parent_map, reconstruct_path(parent_map, start, goal)

        for dr, dc in get_directions():
            neighbor = (curr[0] + dr, curr[1] + dc)
            new_g = g + 1
            if is_valid(maze, neighbor[0], neighbor[1]) and not is_wall(maze, neighbor[0], neighbor[1]):
                if neighbor not in visited_g or new_g < visited_g[neighbor]:
                    visited_g[neighbor] = new_g
                    parent_map[neighbor] = curr
                    f_score = new_g + manhattan_distance(neighbor, goal)
                    heapq.heappush(pq, (f_score, new_g, neighbor))
    return parent_map, []

def draw_search_tree(parent_map, path, start, goal, filename , mode = "LR"):
    start, goal = tuple(start), tuple(goal)
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir=mode, nodesep='0.4', ranksep='0.5')
    
    path_set = set(path)
    path_edges = set(zip(path, path[1:]))
    all_nodes = set(parent_map.keys()) | set(parent_map.values())

    for node in all_nodes:
        name = str(node)
        lbl = f"{node[0]},{node[1]}"
        if node == goal:
            dot.node(name, label=lbl, style='filled', fillcolor='palegreen', shape='doublecircle')
        elif node == start:
            dot.node(name, label=lbl, style='filled', fillcolor='lightblue', shape='diamond')
        elif node in path_set:
            dot.node(name, label=lbl, style='filled', fillcolor='lightyellow')
        else:
            dot.node(name, label=lbl, color='gray70', fontcolor='gray40')

    for child, parent in parent_map.items():
        if (parent, child) in path_edges:
            dot.edge(str(parent), str(child), color='blue', penwidth='2.5')
        else:
            dot.edge(str(parent), str(child), color='gray85', style='dashed')

    dot.render(filename, cleanup=True)
    print(f"Graph saved as {filename}.png")


if __name__ == "__main__":
    maze =  [
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
  ]
    start_node = (0, 0)
    goal_node = (9, 4)

    parents, final_path = dfs(maze, start_node, goal_node)
    
    draw_search_tree(parents, final_path, start_node, goal_node, "maze_result_DFS" , "TB")
    parents, final_path = bfs(maze, start_node, goal_node)
    
    draw_search_tree(parents, final_path, start_node, goal_node, "maze_result_BFS")
    parents, final_path = a_star(maze, start_node, goal_node)
    
    draw_search_tree(parents, final_path, start_node, goal_node, "maze_result_A*")