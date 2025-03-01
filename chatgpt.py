import pygame
import random
from collections import deque

# Configuración básica
WIDTH, HEIGHT = 448, 496
TILE_SIZE = 32
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
FPS = 10

# Colores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Mapa del nivel (1 = pared, 0 = camino)
LEVEL = [
    "1111111111111111111111111",
    "1000000000110000000000001",
    "1011111010110111011111101",
    "1010001010000001000000101",
    "1010111110111111011110101",
    "1000000000100001000000001",
    "1111011110110111011110111",
    "1001010000000000001010001",
    "1011111010110111011111101",
    "1000001010000001000000101",
    "1111011110110111011110111",
    "1000000000100001000000001",
    "1111111111111111111111111",
]

# Cargar el mapa
walls = set()
pacman_pos = (1, 1)
ghost_positions = [(10, 1), (12, 10), (1, 10), (5, 5)]

def load_level():
    for row_idx, row in enumerate(LEVEL):
        for col_idx, tile in enumerate(row):
            if tile == "1":
                walls.add((col_idx, row_idx))

def draw_level(screen):
    for wall in walls:
        pygame.draw.rect(screen, BLUE, (wall[0] * TILE_SIZE, wall[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def move_entity(position, direction):
    new_pos = (position[0] + direction[0], position[1] + direction[1])
    if new_pos not in walls:
        return new_pos
    return position

class Ghost:
    def __init__(self, x, y, color, behavior):
        self.position = (x, y)
        self.color = color
        self.behavior = behavior

    def move(self, pacman_pos, ghosts):
        if self.behavior == "random":
            self.position = move_entity(self.position, random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)]))
        elif self.behavior == "chaser":
            self.position = self.a_star(pacman_pos)
        elif self.behavior == "ambusher":
            target = (pacman_pos[0] + 2, pacman_pos[1])
            self.position = self.a_star(target)
        elif self.behavior == "hunter":
            target = ghosts[0].position  # Persigue al fantasma perseguidor para acorralar a Pac-Man
            self.position = self.a_star(target)

    def a_star(self, target):
        queue = deque([(self.position, [])])
        visited = set()
        while queue:
            (current, path) = queue.popleft()
            if current == target:
                return path[0] if path else self.position
            if current in visited:
                continue
            visited.add(current)
            for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (current[0] + d[0], current[1] + d[1])
                if next_pos not in walls and next_pos not in visited:
                    queue.append((next_pos, path + [next_pos]))
        return self.position

# Inicializar juego
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
load_level()

ghosts = [
    Ghost(10, 1, RED, "chaser"),
    Ghost(12, 10, PINK, "ambusher"),
    Ghost(1, 10, GREEN, "hunter"),
    Ghost(5, 5, WHITE, "random"),
]

direction = (0, 0)
running = True
while running:
    screen.fill(BLACK)
    draw_level(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                direction = (1, 0)
    
    pacman_pos = move_entity(pacman_pos, direction)
    pygame.draw.circle(screen, YELLOW, (pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2, pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)
    
    for ghost in ghosts:
        ghost.move(pacman_pos, ghosts)
        pygame.draw.rect(screen, ghost.color, (ghost.position[0] * TILE_SIZE, ghost.position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
