import heapq

def distance(coord1, coord2):
    # Función para calcular la distancia entre dos coordenadas (euclidiana)
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

class Node:
    def __init__(self, coord):
        self.coord = coord
        self.g = float('inf')  # Coste real desde el inicio
        self.h = 0  # Heurística (distancia estimada al final)
        self.parent = None

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

def astar(start, end, obstacles_map):
    open_list = []
    closed_set = set()

    start_node = Node(start)
    end_node = Node(end)

    start_node.g = 0
    start_node.h = distance(start, end)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.coord == end:
            path = []
            while current_node:
                path.append(current_node.coord)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node.coord)

        x, y = current_node.coord
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
            if (
                neighbor_coord[0] < 0 or neighbor_coord[0] >= len(obstacles_map) or
                neighbor_coord[1] < 0 or neighbor_coord[1] >= len(obstacles_map[0])
            ):
                continue

            if obstacles_map[neighbor_coord[0]][neighbor_coord[1]].tipo == 1 or neighbor_coord in closed_set:
                continue

            neighbor = Node(neighbor_coord)
            tentative_g = current_node.g + distance(current_node.coord, neighbor.coord)

            if tentative_g < neighbor.g:
                neighbor.parent = current_node
                neighbor.g = tentative_g
                neighbor.h = distance(neighbor.coord, end)

                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)

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