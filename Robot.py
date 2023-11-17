from enum import Enum
from Casilla import *
from Algoritmo import *
from collections import deque
import numpy as np
from Aestrella import *

class Robot:

    VIEWPORT_RADIUS = 10

    def __init__(self, mapaGlobal, coordenadas, campoVision, niebla):
        self.mapaGlobal = mapaGlobal
        self.niebla = niebla
        self.campoVision = campoVision
        self.coordenadas = coordenadas

        self.alto = len(mapaGlobal)
        self.ancho = len(mapaGlobal[0])

        #self.mapaLocal =[[Casilla() for _ in range(self.ancho)] for _ in range(self.alto)]
        self.mapaLocal = niebla
        self.bfsQueue = deque([coordenadas])
        self.siguiendoAEstrella = False
        self.rutaAEstrella = None

    def moverse(self):
        if self.siguiendoAEstrella:
            self.seguirRuta()

        if self.siguiendoAEstrella is False:
        # Hay victima ? Ir a victima : Ir a niebla
        # if self.mapaLocal[self.coordenadas[0]][self.coordenadas[1]].tipoObjetivo is TipoObjetivo.LIBRE:
        #     self.rutaAEstrella = astar(self.coordenadas, self.find_nearest_fog(), self.mapaLocal)
        #     self.siguiendoAEstrella = True
        # else:
        
            nieblas_cercanas = self.find_nearest_fog()
            print("Niebla cercana ", nieblas_cercanas)
            
            # Do (find A* path to nearest fog) while A* path is empty
            while True:
                niebla_mas_cercana = nieblas_cercanas.pop(-1)
                print("Niebla mas cercana ",niebla_mas_cercana)
                
                self.rutaAEstrella = astar(self.coordenadas, niebla_mas_cercana, self.mapaLocal)
                print("Ruta A* ",self.rutaAEstrella)
                if self.rutaAEstrella != None:
                    break
            self.siguiendoAEstrella = True
            self.seguirRuta()
            
        





















        
            # if not self.bfsQueue:
            #     return False

            # # Ir haciendo pop hasta que encontremos uno que almenos 1 vecino no este visitado.
            # current_row, current_col = self.bfsQueue.pop()
            # neighbors = [(current_row - 1, current_col), (current_row + 1, current_col),
            #              (current_row, current_col - 1), (current_row, current_col + 1),
            #              (current_row - 1, current_col - 1), (current_row + 1, current_col + 1),
            #              (current_row - 1, current_col +1), (current_row + 1, current_col -1)]

            # if self.mePuedoMoverSinDarSaltos(current_row, current_col):
            #     self.coordenadas = (current_row, current_col)
            # else:
            #     self.rutaAEstrella = astar(self.coordenadas, (current_row, current_col), self.mapaLocal)
            #     self.siguiendoAEstrella = True


            # for neighbor_row, neighbor_col in neighbors:
            #     if self.is_valid_move(neighbor_row, neighbor_col):
            #         self.bfsQueue.append((neighbor_row, neighbor_col))

            #         self.mapaLocal[neighbor_row][neighbor_col].tipo = TipoCasilla.VISITADO
            #         self.mapaGlobal[neighbor_row][neighbor_col].tipo = TipoCasilla.VISITADO
            #         self.quitar_niebla()

            return True

    def mePuedoMoverSinDarSaltos(self, nuevaX, nuevaY):
        difX = abs(self.coordenadas[0] - nuevaX)
        difY = abs(self.coordenadas[1] - nuevaY)

        return difY < 2 and difX < 2

    def is_valid_move(self, row, col):
        rows, cols = self.alto, self.ancho

        # TODO Simplificar
        dentroDeLosLimites = 0 <= row < rows and 0 <= col < cols
        noHayPared = self.mapaGlobal[row][col].tipo is TipoCasilla.NADA
        noLoHeVisitado = self.mapaLocal[row][col].tipo is not TipoCasilla.VISITADO

        return dentroDeLosLimites and noHayPared and noLoHeVisitado
    
    def quitar_niebla(self):
        robot_x, robot_y = self.coordenadas
        for i in range(max(0, robot_x - self.VIEWPORT_RADIUS), min(self.alto, robot_x + self.VIEWPORT_RADIUS + 1)):
            for j in range(max(0, robot_y - self.VIEWPORT_RADIUS), min(self.ancho, robot_y + self.VIEWPORT_RADIUS + 1)):
                distance = np.sqrt((i - robot_x) ** 2 + (j - robot_y) ** 2)
                if distance <= self.VIEWPORT_RADIUS:
                    self.niebla[i][j].tipo = self.mapaGlobal[i][j].tipo
                    self.mapaLocal[i][j].tipo = self.mapaGlobal[i][j].tipo

    def find_nearest_fog(self):
        robot_x, robot_y = self.coordenadas
        nearest_fogs = []
        #nearest_fog = None
        min_distance = float('inf')
                        
        for i in range(max(0, robot_x - self.VIEWPORT_RADIUS), min(self.alto, robot_x + self.VIEWPORT_RADIUS + 1)):
            for j in range(max(0, robot_y - self.VIEWPORT_RADIUS), min(self.ancho, robot_y + self.VIEWPORT_RADIUS + 1)):
                if self.mapaLocal[i][j].tipo == TipoCasilla.NIEBLA:
                    distance = abs(i - robot_x) + abs(j - robot_y)
                    if distance <= min_distance:
                        min_distance = distance
                        #nearest_fog = (i, j)
                        nearest_fogs.append((i, j))


        return nearest_fogs
    
    def seguirRuta(self):
        self.coordenadas = self.rutaAEstrella.pop(0)
        self.quitar_niebla()
        if len(self.rutaAEstrella) == 0:
            self.siguiendoAEstrella = False