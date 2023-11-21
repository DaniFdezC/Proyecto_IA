#import heapq
import math


from Casilla import *

def distance(coord1, coord2):
    # Función para calcular la distancia entre dos coordenadas (euclidiana)
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

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

def astar(start, end, obstacles_map, pygame, pantalla, type):
    alto = len(obstacles_map)
    ancho = len(obstacles_map[0])
    steps = 0
    open_list = []
    closed_set = set()

    start_node = Node(start)
    end_node = Node(end)

    start_node.g = 0
    start_node.h = distance(start, end)

    # heapq.heappush(open_list, start_node)
    open_list.append(start_node)

    while open_list:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_set.add(current_node.coord)
        #print(" -- Current", current_node.coord)
        #print(" -- End -- ", end, (alto, ancho))
        if current_node.coord == end:
            path = []
            while current_node:
                path.append(current_node.coord)
                current_node = current_node.parent
            if len(path) > 1: # Para que no se pare en la niebla
                path.pop(0)
            return path[::-1]


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
            if steps > 30000:
                return None
            
            # pygame.draw.rect(pantalla, (229, 137, 194), (neighbor_coord[1] * 5, neighbor_coord[0] * 5, 5, 5))
            # pygame.display.flip()
            
            #if (neighbor_coord == end):
                #print("END! ", neighbor_coord)
                #print("0 ", ancho)
                #print("1 ", alto)
            
            if (
                neighbor_coord[0] < 0 or neighbor_coord[0] >= alto or
                neighbor_coord[1] < 0 or neighbor_coord[1] >= ancho or
                neighbor_coord in closed_set
            ):
                continue
            
            #print("A* --> ", neighbor_coord,  obstacles_map[neighbor_coord[1]][neighbor_coord[0]].tipo, obstacles_map[neighbor_coord[1]][neighbor_coord[0]].tipo != TipoCasilla.NADA)
           # print("Current neighbor", neighbor_coord, obstacles_map[neighbor_coord[0]][neighbor_coord[1]].tipo )
           # print("Closed Set", closed_set)
            if (obstacles_map[neighbor_coord[0]][neighbor_coord[1]].tipo == TipoCasilla.NIEBLA and type != "victima"):
               print("TOQUE NIEBLA! ", neighbor_coord)
               end = neighbor_coord
            elif ((obstacles_map[neighbor_coord[0]][neighbor_coord[1]].tipo != TipoCasilla.NADA and neighbor_coord != end)):
                closed_set.add(neighbor_coord)
                continue

            neighbor = Node(neighbor_coord)

            # Create the f, g, and h values
            neighbor.g = current_node.g + hypot(current_node.coord, neighbor.coord)
            neighbor.h = distance(neighbor.coord, end)
            neighbor.f = neighbor.g + neighbor.h

            exixts = False
            # Child is already in the open list
            for open_node in open_list:
                if neighbor.coord == open_node.coord and neighbor.g > open_node.g:
                    exixts = True
                    break 
            
            if exixts:
                break
            neighbor.parent = current_node
            open_list.append(neighbor)
            pygame.draw.rect(pantalla, (0, 255, 255), (neighbor_coord[1] * 5, neighbor_coord[0] * 5, 5, 5))
            pygame.display.flip()

            # tentative_g = current_node.g + 

            # if tentative_g < neighbor.g:
            #     neighbor.parent = current_node
            #     neighbor.g = tentative_g
            #     neighbor.h = distance(neighbor.coord, end)

            #     if neighbor not in open_list:
            #         open_list.append(neighbor)
                   

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