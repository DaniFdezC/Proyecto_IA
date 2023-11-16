from enum import Enum
from Casilla import *
from Algoritmo import *
from collections import deque
from Aestrella import *

class Robot:

    def __init__(self, mapaGlobal, coordenadas, campoVision):
        self.mapaGlobal = mapaGlobal
        self.coordenadas = coordenadas
        self.campoVision = campoVision

        self.mapaLocal =[[Casilla() for _ in range(len(mapaGlobal[0]))] for _ in range(len(mapaGlobal))]
        self.bfsQueue = deque([coordenadas])
        self.siguiendoAEstrella = False
        self.rutaAEstrella = None
        self.indiceRuta = 1

    def moverse(self):
        if self.siguiendoAEstrella:
            self.coordenadas = self.rutaAEstrella[self.indiceRuta]
            self.indiceRuta += 1
            if len(self.rutaAEstrella) >= self.indiceRuta:
                self.siguiendoAEstrella = False
                self.indiceRuta = 1

        if self.siguiendoAEstrella is False:
            if not self.bfsQueue:
                return False

            # Ir haciendo pop hasta que encontremos uno que almenos 1 vecino no este visitado.
            current_row, current_col = self.bfsQueue.pop()
            neighbors = [(current_row - 1, current_col), (current_row + 1, current_col),
                         (current_row, current_col - 1), (current_row, current_col + 1),
                         (current_row - 1, current_col - 1), (current_row + 1, current_col + 1),
                         (current_row - 1, current_col +1), (current_row + 1, current_col -1)]

            if self.mePuedoMoverSinDarSaltos(current_row, current_col):
                self.coordenadas = (current_row, current_col)
            else:
                self.rutaAEstrella = astar(self.coordenadas, (current_row, current_col), self.mapaLocal)
                self.siguiendoAEstrella = True


            for neighbor_row, neighbor_col in neighbors:
                if self.is_valid_move(neighbor_row, neighbor_col):
                    self.bfsQueue.append((neighbor_row, neighbor_col))

                    self.mapaLocal[neighbor_row][neighbor_col].tipo = TipoCasilla.VISITADO
                    self.mapaGlobal[neighbor_row][neighbor_col].tipo = TipoCasilla.VISITADO

            return True

    def mePuedoMoverSinDarSaltos(self, nuevaX, nuevaY):
        difX = abs(self.coordenadas[0] - nuevaX)
        difY = abs(self.coordenadas[1] - nuevaY)

        return difY < 2 and difX < 2


    def is_valid_move(self, row, col):
        rows, cols = len(self.mapaGlobal), len(self.mapaGlobal[0])

        # TODO Simplificar
        dentroDeLosLimites = 0 <= row < rows and 0 <= col < cols
        noHayPared = self.mapaGlobal[row][col].tipo is TipoCasilla.NADA
        noLoHeVisitado = self.mapaLocal[row][col].tipo is not TipoCasilla.VISITADO

        return dentroDeLosLimites and noHayPared and noLoHeVisitado
