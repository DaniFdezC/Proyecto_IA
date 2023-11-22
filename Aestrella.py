import heapq

from Casilla import *
from typing import *


def distancia(coord1: Tuple[int, int], coord2: Tuple[int, int]) -> int:
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


class Node:
    def __init__(self, coordenadas: Tuple[int, int], g: int, h: int, parent=None):
        self.coord = coordenadas
        self.g = g  # Coste real desde el inicio
        self.h = h  # Heurística (distancia estimada al final)
        self.parent: Node = parent

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)


def astar(start: Tuple[int, int], end: Tuple[int, int], mapaLocal: List[List[Casilla]]) -> List[Tuple[int, int]]:
    openList: List[Node] = []
    closedSet: Set[Tuple[int, int]] = set()

    heapq.heappush(openList, Node(coordenadas=start, g=0, h=distancia(start, end)))

    while openList:
        nodoActual: Node = heapq.heappop(openList)

        if nodoActual.coord == end:
            path: List[Tuple[int, int]] = []

            while nodoActual:
                path.append(nodoActual.coord)
                nodoActual = nodoActual.parent
            path = path[::-1]
            del path[0]
            return path

        closedSet.add(nodoActual.coord)

        x, y = nodoActual.coord
        coordenadasVecinas = [
            (x - 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y),
            (x + 1, y),
            (x + 1, y - 1),
            (x + 1, y + 1),
            (x, y - 1),
            (x, y + 1)
        ]

        for coordenadaVecina in coordenadasVecinas:
            coordenadaVecinaX = coordenadaVecina[0]
            coordenadaVecinaY = coordenadaVecina[1]
            maxX = len(mapaLocal[0])
            maxY = len(mapaLocal)

            if (
                    coordenadaVecinaX < 0 or coordenadaVecinaX >= maxX or
                    coordenadaVecinaY < 0 or coordenadaVecinaY >= maxY or
                    mapaLocal[coordenadaVecinaY][coordenadaVecinaX].tipo is TipoCasilla.NADA or
                    mapaLocal[coordenadaVecinaY][coordenadaVecinaX].tipo is TipoCasilla.PARED or
                    coordenadaVecina in closedSet
            ):
                continue

            nuevaG = nodoActual.g + 1
            nuevaH = distancia(coordenadaVecina, end)

            for node in openList:
                if node.coord == coordenadaVecina and node.g <= nuevaG:
                    break
            else: # El else se ejecutara si no se ha ejectado el break del if de arriba
                heapq.heappush(openList, Node(coordenadas=coordenadaVecina, g=nuevaG, h=nuevaH, parent=nodoActual))

    return None

# # Ejemplo de uso:
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
