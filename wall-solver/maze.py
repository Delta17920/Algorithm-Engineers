import pygame
import random
from settings import *
from cell import Cell

class Maze:
    def __init__(self, screen, should_generate=False):
        self.screen = screen
        self.cols = WIDTH // TILE_SIZE
        self.rows = HEIGHT // TILE_SIZE
        self.grid_cells = [[Cell(col, row) for row in range(self.rows)] for col in range(self.cols)]
        if should_generate:
            self.generate_maze()

    def draw(self):
        self.screen.fill(GREY)
        for col in range(self.cols):
            for row in range(self.rows):
                self.grid_cells[col][row].draw(self.screen)

    def remove_wall(self, current, next_cell):
        dx, dy = current.x - next_cell.x, current.y - next_cell.y
        if dx == 1: current.walls['left'], next_cell.walls['right'] = False, False
        elif dx == -1: current.walls['right'], next_cell.walls['left'] = False, False
        if dy == 1: current.walls['top'], next_cell.walls['bottom'] = False, False
        elif dy == -1: current.walls['bottom'], next_cell.walls['top'] = False, False

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        x, y = cell.x, cell.y
        if y > 0 and not self.grid_cells[x][y-1].visited: neighbors.append(self.grid_cells[x][y-1])
        if x < self.cols - 1 and not self.grid_cells[x+1][y].visited: neighbors.append(self.grid_cells[x+1][y])
        if y < self.rows - 1 and not self.grid_cells[x][y+1].visited: neighbors.append(self.grid_cells[x][y+1])
        if x > 0 and not self.grid_cells[x-1][y].visited: neighbors.append(self.grid_cells[x-1][y])
        return random.choice(neighbors) if neighbors else None

    def generate_maze(self):
        current_cell = self.grid_cells[0][0]
        stack = []
        while True:
            current_cell.visited = True
            next_cell = self.get_unvisited_neighbors(current_cell)
            if next_cell:
                next_cell.visited = True
                stack.append(current_cell)
                self.remove_wall(current_cell, next_cell)
                current_cell = next_cell
            elif stack: current_cell = stack.pop()
            else: break
        for row in self.grid_cells:
            for cell in row: cell.visited = False