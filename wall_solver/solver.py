from collections import deque
import heapq

def get_valid_neighbors(maze, cell):
    """Finds neighbors you can move to, but ONLY if they are part of the known/explored map."""
    neighbors = []
    x, y = cell.x, cell.y
    if not cell.walls['top'] and y > 0 and maze.grid_cells[x][y-1].explored:
        neighbors.append(maze.grid_cells[x][y-1])
    if not cell.walls['right'] and x < maze.cols - 1 and maze.grid_cells[x+1][y].explored:
        neighbors.append(maze.grid_cells[x+1][y])
    if not cell.walls['bottom'] and y < maze.rows - 1 and maze.grid_cells[x][y+1].explored:
        neighbors.append(maze.grid_cells[x][y+1])
    if not cell.walls['left'] and x > 0 and maze.grid_cells[x-1][y].explored:
        neighbors.append(maze.grid_cells[x-1][y])
    return neighbors

def heuristic(cell1, cell2):
    return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

def solve_bfs(maze, start_cell, end_cell):
    queue = deque([start_cell])
    came_from = {start_cell: None}
    while queue:
        current_cell = queue.popleft()
        if current_cell == end_cell: break
        for next_cell in get_valid_neighbors(maze, current_cell):
            if next_cell not in came_from:
                queue.append(next_cell)
                came_from[next_cell] = current_cell
                yield next_cell
    return came_from

def solve_astar(maze, start_cell, end_cell):
    count = 0
    open_set = [(0, count, start_cell)]
    came_from = {start_cell: None}
    g_score = {cell: float("inf") for col in maze.grid_cells for cell in col}
    g_score[start_cell] = 0
    f_score = {cell: float("inf") for col in maze.grid_cells for cell in col}
    f_score[start_cell] = heuristic(start_cell, end_cell)
    while open_set:
        current_cell = heapq.heappop(open_set)[2]
        if current_cell == end_cell: break
        for neighbor in get_valid_neighbors(maze, current_cell):
            temp_g_score = g_score[current_cell] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_cell
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end_cell)
                if not any(neighbor == item[2] for item in open_set):
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    yield neighbor
    return came_from

def solve_dijkstra(maze, start_cell, end_cell):
    count = 0
    open_set = [(0, count, start_cell)]
    came_from = {start_cell: None}
    g_score = {cell: float("inf") for col in maze.grid_cells for cell in col}
    g_score[start_cell] = 0
    while open_set:
        current_cell = heapq.heappop(open_set)[2]
        if current_cell == end_cell: break
        for neighbor in get_valid_neighbors(maze, current_cell):
            temp_g_score = g_score[current_cell] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_cell
                g_score[neighbor] = temp_g_score
                if not any(neighbor == item[2] for item in open_set):
                    count += 1
                    heapq.heappush(open_set, (g_score[neighbor], count, neighbor))
                    yield neighbor
    return came_from