from enum import Enum
from Casilla import *
from Algoritmo import *
from collections import deque

class Robot:

    def __init__(self, mapaGlobal, coordenadas, campoVision):
        self.mapaGlobal = mapaGlobal
        self.coordenadas = coordenadas
        self.campoVision = campoVision

        self.mapaLocal =[[Casilla() for _ in range(len(mapaGlobal[0]))] for _ in range(len(mapaGlobal))]
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

        return True

    def is_valid_move(self, row, col):
        rows, cols = len(self.mapaGlobal), len(self.mapaGlobal[0])

        # TODO Simplificar
        dentroDeLosLimites = 0 <= row < rows and 0 <= col < cols
        noHayPared = self.mapaGlobal[row][col].tipo is TipoCasilla.NADA
        noLoHeVisitado = self.mapaLocal[row][col].tipo is not TipoCasilla.VISITADO

        return dentroDeLosLimites and noHayPared and noLoHeVisitado
