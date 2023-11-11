## Autor: Manuel Ortega con ayuda de ChatGPT y https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

import pygame
import sys
import math
import heapq

# Configuración de Pygame
pygame.init()

# Tamaño de la pantalla y colores
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Crear la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Path Planning con Obstáculos")

# Clase para representar el nodo del mapa
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.parent = None
        self.g = 0
        self.h = 0
        self.is_obstacle = False

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

# Función para calcular la distancia entre dos nodos
def distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

# Crear el mapa y agregar obstáculos
grid = [[Node(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]

# Definir nodos de inicio y objetivo
start_node = grid[5][5]
end_node = grid[15][15]

# Definir vecinos de cada nodo
for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        node = grid[x][y]
        if x > 0:
            node.neighbors.append(grid[x - 1][y])
        if x < GRID_WIDTH - 1:
            node.neighbors.append(grid[x + 1][y])
        if x > 0 and y > 0:
            node.neighbors.append(grid[x - 1][y - 1])
        if x < GRID_WIDTH - 1 and y < GRID_HEIGHT - 1:
            node.neighbors.append(grid[x + 1][y + 1])
        if y > 0:
            node.neighbors.append(grid[x][y - 1])
        if y < GRID_HEIGHT - 1:
            node.neighbors.append(grid[x][y + 1])
        if x > 0 and y < GRID_HEIGHT - 1:
            node.neighbors.append(grid[x - 1][y + 1])
        if x < GRID_WIDTH - 1 and y > 0:
            node.neighbors.append(grid[x + 1][y - 1])
                    
# Agregar obstáculos manualmente (puedes personalizar esto)
obstacle_nodes = [
    grid[7][7],
    grid[8][7],
    grid[9][7],
    grid[10][7],
    grid[11][7],
    grid[12][7],
    grid[13][7],
    grid[14][7],
    grid[15][7],
    grid[16][7],
    grid[10][8],
    grid[10][9],
    grid[10][10],
    grid[10][11],
    grid[10][12],
    grid[10][13],
    grid[10][14],
]

for node in obstacle_nodes:
    node.is_obstacle = True

# Función para realizar la búsqueda A*
def astar(start, end):
    open_list = []
    closed_set = set()

    heapq.heappush(open_list, start)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node == end:
            path = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node)

        for neighbor in current_node.neighbors:
            if neighbor.is_obstacle or neighbor in closed_set:
                continue

            tentative_g = current_node.g + distance(current_node, neighbor)

            if neighbor not in open_list or tentative_g < neighbor.g:
                neighbor.parent = current_node
                neighbor.g = tentative_g
                neighbor.h = distance(neighbor, end)

                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)

    return None

# Función para dibujar el mapa
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            node = grid[x][y]
            color = WHITE if not node.is_obstacle else BLACK
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

# Función para dibujar el camino
def draw_path(path):
    for node in path:
        pygame.draw.rect(screen, BLUE, (node.x * GRID_SIZE, node.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Bucle principal
running = True
finding_path = False
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not finding_path:
            x, y = pygame.mouse.get_pos()
            start_node = grid[x // GRID_SIZE][y // GRID_SIZE]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not finding_path:
                x, y = pygame.mouse.get_pos()
                end_node = grid[x // GRID_SIZE][y // GRID_SIZE]
                finding_path = True

    draw_grid()
    if finding_path:
        path = astar(start_node, end_node)
        if path:
            draw_path(path)

    pygame.draw.rect(screen, GREEN, (start_node.x * GRID_SIZE, start_node.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, RED, (end_node.x * GRID_SIZE, end_node.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()

pygame.quit()
sys.exit()