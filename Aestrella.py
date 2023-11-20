import heapq

from Casilla import *

def distance(coord1, coord2):
    # Función para calcular la distancia entre dos coordenadas (euclidiana)
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

class Node:
    def __init__(self, coord):
        self.coord = coord
        self.g = float("inf")  # Coste del camino desde el inicio
        self.h = 0  # Heurística (distancia estimada al final)
        self.parent = None

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

def astar(start, end, obstacles_map, pygame, pantalla, type):
    steps = 0
    open_list = []
    closed_set = set()

    start_node = Node(start)
    end_node = Node(end)

    start_node.g = 0
    start_node.h = distance(start, end)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
       # print(" -- Current", current_node.coord)
       # print(" -- End -- ", end)
        if current_node.coord == end:
            path = []
            while current_node:
                path.append(current_node.coord)
                current_node = current_node.parent
            if len(path) > 1: # Para que no se pare en la niebla
                path.pop(0)
            return path[::-1]

        closed_set.add(current_node.coord)

        x, y = current_node.coord
        pygame.draw.rect(pantalla, (255, 0, 0), (y * 5, x * 5, 5, 5))
        pygame.display.flip()
       # print("--- Movimiento a ", current_node.coord)
        neighbors = [
            (x - 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y),
            (x + 1, y),
            (x + 1, y - 1),
            (x + 1, y + 1),
            (x, y - 1),
            (x, y + 1)
        ]

        for neighbor_coord in neighbors:
            steps += 1
            if steps > 10000:
                return None
            
            pygame.draw.rect(pantalla, (229, 137, 194), (neighbor_coord[1] * 5, neighbor_coord[0] * 5, 5, 5))
            pygame.display.flip()
            
            if (
                neighbor_coord[0] < 0 or neighbor_coord[0] >= len(obstacles_map[0]) or
                neighbor_coord[1] < 0 or neighbor_coord[1] >= len(obstacles_map) or
                neighbor_coord in closed_set
            ):
                continue
            
            #print("A* --> ", neighbor_coord,  obstacles_map[neighbor_coord[1]][neighbor_coord[0]].tipo, obstacles_map[neighbor_coord[1]][neighbor_coord[0]].tipo != TipoCasilla.NADA)
            if (obstacles_map[neighbor_coord[0]][neighbor_coord[1]].tipo == TipoCasilla.NIEBLA and type != "victima"):
                end = neighbor_coord
                heapq.heappush(open_list, neighbor)
                pygame.draw.rect(pantalla, (0, 255, 255), (neighbor_coord[1] * 5, neighbor_coord[0] * 5, 5, 5))
                pygame.display.flip()
                break
            elif ((obstacles_map[neighbor_coord[0]][neighbor_coord[1]].tipo != TipoCasilla.NADA and neighbor_coord != end)):
                continue

            neighbor = Node(neighbor_coord)
            tentative_g = current_node.g + distance(current_node.coord, neighbor.coord)

            if tentative_g < neighbor.g:
                neighbor.parent = current_node
                neighbor.g = tentative_g
                neighbor.h = distance(neighbor.coord, end)

                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)
                    pygame.draw.rect(pantalla, (0, 255, 255), (neighbor_coord[1] * 5, neighbor_coord[0] * 5, 5, 5))
                    pygame.display.flip()

    return None

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