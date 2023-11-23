#import heapq
import math
from Casilla import *

# Usada para calcular el coste h
def distance(coord1, coord2):
    # Función para calcular la distancia entre dos coordenadas (euclidiana)
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Usada para calcular valores 1 y 1.4... para el coste g
def hypot(coord1, coord2):
    return math.hypot(coord1[0] - coord2[0], coord1[1] - coord2[1])

class Node:
    def __init__(self, coord):
        self.coord = coord
        self.g = 0  # Coste del camino desde el inicio
        self.h = 0  # Heurística (distancia estimada al final)
        self.f = 0  # Coste total
        self.parent = None

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

def astar(start, end, obstacles_map, pygame, pantalla, type = "explorar"):
    alto = len(obstacles_map)
    ancho = len(obstacles_map[0])
    steps = 0
    open_list = []
    closed_set = set()

    start_node = Node(start)

    start_node.g = 0
    start_node.h = distance(start, end)

    open_list.append(start_node)

    while open_list:
        
        current_node = min(open_list, key=lambda node: node.f)
        
        open_list.remove(current_node)
        closed_set.add(current_node.coord)
        
        if current_node.coord == end:
            path = []
            while current_node:
                path.append(current_node.coord)
                current_node = current_node.parent
            if len(path) > 1 and type != "victima": # Para que no se pare en la niebla
                path.pop(0)
            if type == "victima":
                print("Camino Hacia Victima ", path)
            return path[::-1]

        x, y = current_node.coord
        # pygame.draw.rect(pantalla, (255, 0, 0), (y * 5, x * 5, 5, 5))
        # pygame.display.flip()
        neighbors = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1)
        ]

        for neighbor_coord in neighbors:
            steps += 1
            if steps > 30000:
                print("No se encontro camino")
                return None
            
            if (
                neighbor_coord[0] < 0 or neighbor_coord[0] >= alto or
                neighbor_coord[1] < 0 or neighbor_coord[1] >= ancho or
                neighbor_coord in closed_set
            ):
                continue
            
            if ((obstacles_map[neighbor_coord[0]][neighbor_coord[1]].tipo == TipoCasilla.NIEBLA) and (type == "explorar")):
               print("TOQUE NIEBLA! ", neighbor_coord, type)
               end = neighbor_coord
               process_neighbor(neighbor_coord, current_node, end, open_list, pantalla, pygame)
               break
            elif ((obstacles_map[neighbor_coord[0]][neighbor_coord[1]].tipo not in [TipoCasilla.NADA, TipoCasilla.RESCATADO, TipoCasilla.VICTIMA, TipoCasilla.ROBOT]) and (neighbor_coord != end)):
                closed_set.add(neighbor_coord)
                continue
            
            process_neighbor(neighbor_coord, current_node, end, open_list, pantalla, pygame)
                   
    print("No se encontro camino")
    return None

def process_neighbor(neighbor_coord, current_node, end, open_list, pantalla, pygame):
        neighbor = Node(neighbor_coord)
        neighbor.parent = current_node

        # Create the f, g, and h values
        neighbor.g = current_node.g + hypot(current_node.coord, neighbor.coord)
        neighbor.h = distance(neighbor.coord, end)
        neighbor.f = neighbor.g + neighbor.h

        exists = False
        # Child is already in the open list
        for open_node in open_list:
            if neighbor.coord == open_node.coord and neighbor.g >= open_node.g:
                exists = True
                break 

        if exists:
            return
        open_list.append(neighbor)
        # pygame.draw.rect(pantalla, (0, 255, 255), (neighbor_coord[1] * 5, neighbor_coord[0] * 5, 5, 5))
        # pygame.display.flip()

# Ejemplo de uso:
# start_coord = (0, 0)
# end_coord = (4, 4)
# obstacles = [ # Casilas en vez de numeros
#     [0, 0, 0, 0, 0],
#     [0, 1, 1, 0, 0],
#     [0, 1, 0, 0, 0],
#     [0, 0, 0, 1, 0],
#     [0, 0, 0, 1, 0]
# ]

# result = astar(start_coord, end_coord, obstacles)
# print(result)