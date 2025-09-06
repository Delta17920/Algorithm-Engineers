import pygame
from settings import *

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.explored = False
        self.visited = False

    def draw(self, screen):
        x_px, y_px = self.x * TILE_SIZE, self.y * TILE_SIZE

        if not self.explored:
            pygame.draw.rect(screen, GREY, (x_px, y_px, TILE_SIZE, TILE_SIZE))
            return

        pygame.draw.rect(screen, WHITE, (x_px, y_px, TILE_SIZE, TILE_SIZE))

        if self.walls['top']:
            pygame.draw.line(screen, BLACK, (x_px, y_px), (x_px + TILE_SIZE, y_px), 2)
        if self.walls['right']:
            pygame.draw.line(screen, BLACK, (x_px + TILE_SIZE, y_px), (x_px + TILE_SIZE, y_px + TILE_SIZE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x_px + TILE_SIZE, y_px + TILE_SIZE), (x_px, y_px + TILE_SIZE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, BLACK, (x_px, y_px + TILE_SIZE), (x_px, y_px), 2)

    def draw_highlight(self, screen, color):
        x_px, y_px = self.x * TILE_SIZE, self.y * TILE_SIZE
        pygame.draw.rect(screen, color, (x_px + 2, y_px + 2, TILE_SIZE - 4, TILE_SIZE - 4))