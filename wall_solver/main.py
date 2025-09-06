# main.py
import pygame
import sys
import time
import random
from settings import *
from maze import Maze
from solver import solve_bfs, solve_astar, solve_dijkstra

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Partial Map Solver | 1:BFS 2:A* 3:Dijkstra | R: New Map")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.new_game()

    def new_game(self):
        self.ground_truth_maze = Maze(self.screen, should_generate=True)

        self.known_world_maze = Maze(self.screen)
        
        self.start_cell = self.known_world_maze.grid_cells[0][0]
        self.end_cell = self.known_world_maze.grid_cells[self.known_world_maze.cols - 1][self.known_world_maze.rows - 1]
        
        self.create_partial_map(reveal_percent=0.5) 
        
        self.solver = None
        self.path = []
        self.path_color = None
        self.time_taken = 0.0
        self.solver_name = ""

    def create_partial_map(self, reveal_percent=0.5):
        """Creates a partial map from the ground truth that includes the true solution path."""
        true_solution_path = []
        for row in self.ground_truth_maze.grid_cells:
            for cell in row:
                cell.explored = True

        came_from_gen = solve_bfs(self.ground_truth_maze, self.ground_truth_maze.grid_cells[0][0], self.ground_truth_maze.grid_cells[self.known_world_maze.cols-1][self.known_world_maze.rows-1])
        try:
            while True: next(came_from_gen)
        except StopIteration as e:
            came_from = e.value
        current = self.ground_truth_maze.grid_cells[self.known_world_maze.cols-1][self.known_world_maze.rows-1]
        while current:
            true_solution_path.append(current)
            current = came_from.get(current)
        for cell in true_solution_path:
            known_cell = self.known_world_maze.grid_cells[cell.x][cell.y]
            known_cell.explored = True
            known_cell.walls = cell.walls

        total_cells = self.known_world_maze.cols * self.known_world_maze.rows
        cells_to_reveal = int(total_cells * reveal_percent)
        for _ in range(cells_to_reveal):
            x, y = random.randrange(self.known_world_maze.cols), random.randrange(self.known_world_maze.rows)
            true_cell = self.ground_truth_maze.grid_cells[x][y]
            known_cell = self.known_world_maze.grid_cells[x][y]
            known_cell.explored = True
            known_cell.walls = true_cell.walls
            
    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.solver:
            try:
                explored_cell = next(self.solver)
                if explored_cell != self.start_cell and explored_cell != self.end_cell:
                    explored_cell.draw_highlight(self.screen, PURPLE)
            except StopIteration as e:
                end_time = time.perf_counter()
                self.time_taken = (end_time - self.solve_start_time) * 1000
                self.reconstruct_path(e.value)
                self.solver = None

    def draw(self):
        self.known_world_maze.draw()
        if self.path and self.path_color:
            for cell in self.path:
                if cell != self.start_cell and cell != self.end_cell:
                    cell.draw_highlight(self.screen, self.path_color)
        
        self.start_cell.draw_highlight(self.screen, BLUE)
        self.end_cell.draw_highlight(self.screen, RED)

        if self.time_taken > 0:
            time_text = f"{self.solver_name} Time: {self.time_taken:.2f} ms"
            text_surface = self.font.render(time_text, True, BLACK, WHITE)
            self.screen.blit(text_surface, (10, 10))
            
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.new_game()
                
                if not self.solver:
                    self.path, self.time_taken = [], 0.0
                    solvers = {
                        pygame.K_1: ("BFS", PATH_BFS_COLOR, solve_bfs),
                        pygame.K_2: ("A*", PATH_ASTAR_COLOR, solve_astar),
                        pygame.K_3: ("Dijkstra", PATH_DIJKSTRA_COLOR, solve_dijkstra),
                    }
                    if event.key in solvers:
                        self.solver_name, self.path_color, solver_func = solvers[event.key]
                        self.solve_start_time = time.perf_counter()
                        self.solver = solver_func(self.known_world_maze, self.start_cell, self.end_cell)

    def reconstruct_path(self, came_from):
        if not came_from or self.end_cell not in came_from: return
        current = self.end_cell
        while current:
            self.path.append(current)
            current = came_from.get(current)
        self.path.reverse()

if __name__ == '__main__':
    game = Game()
    game.run()