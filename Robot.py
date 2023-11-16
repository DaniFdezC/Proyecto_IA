from enum import Enum
from Casilla import *
from Algoritmo import *
from collections import deque
import numpy as np

class Robot:

    VIEWPORT_RADIUS = 10

    def __init__(self, mapaGlobal, coordenadas, campoVision, niebla):
        self.mapaGlobal = mapaGlobal
        self.niebla = niebla
        self.campoVision = campoVision
        self.coordenadas = coordenadas

        self.alto = len(mapaGlobal)
        self.ancho = len(mapaGlobal[0])

        self.mapaLocal =[[Casilla() for _ in range(self.ancho)] for _ in range(self.alto)]
        self.bfsQueue = deque([coordenadas])

    def moverse(self):
        if not self.bfsQueue:
            return False

        current_row, current_col = self.bfsQueue.pop()
        neighbors = [(current_row - 1, current_col), (current_row + 1, current_col),
                     (current_row, current_col - 1), (current_row, current_col + 1),
                     (current_row - 1, current_col - 1), (current_row + 1, current_col + 1),
                     (current_row - 1, current_col +1), (current_row + 1, current_col -1)]

        self.coordenadas = (current_row, current_col)

        for neighbor_row, neighbor_col in neighbors:
            if self.is_valid_move(neighbor_row, neighbor_col):
                self.bfsQueue.append((neighbor_row, neighbor_col))
                self.mapaLocal[neighbor_row][neighbor_col].tipo = TipoCasilla.VISITADO
                self.mapaGlobal[neighbor_row][neighbor_col].tipo = TipoCasilla.VISITADO
                self.quitar_niebla()

        return True


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
