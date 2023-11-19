from enum import Enum
from Casilla import *
from Algoritmo import *
from collections import deque
import numpy as np
from Aestrella import *
from typing import *


class Robot:
    VIEWPORT_RADIUS = 10

    def __init__(self, mapaGlobal, coordenadas, campoVision):
        self.mapaGlobal = mapaGlobal
        self.campoVision = campoVision
        self.coordenadas = coordenadas
        self.coordenadasIniciales = coordenadas

        self.alto = len(mapaGlobal)
        self.ancho = len(mapaGlobal[0])

        self.mapaLocal = [[Casilla() for _ in range(self.ancho)] for _ in range(self.alto)]
        self.colaBFS = deque([coordenadas])

        self.siguiendoAEstrella = False
        self.rutaAEstrella = None
        self.indiceRuta = 1

    def moverse(self):
        if self.siguiendoAEstrella:
            self.coordenadas = self.rutaAEstrella[self.indiceRuta]
            self.mapaLocal[self.coordenadas[1]][self.coordenadas[0]].tipo = TipoCasilla.VISITADO
            self.mapaGlobal[self.coordenadas[1]][self.coordenadas[0]].tipo = TipoCasilla.VISITADO
            self.indiceRuta += 1
            if len(self.rutaAEstrella) >= self.indiceRuta:
                self.siguiendoAEstrella = False
                self.indiceRuta = 1

        if self.siguiendoAEstrella is False:
            seguir = True

            while seguir:
                if not self.colaBFS:
                    return False

                columanXActual, filaYActual = self.colaBFS.pop()
                vecinos = [(columanXActual - 1, filaYActual),
                           (columanXActual + 1, filaYActual),
                           (columanXActual, filaYActual - 1),
                           (columanXActual, filaYActual + 1),
                           (columanXActual - 1, filaYActual - 1),
                           (columanXActual + 1, filaYActual + 1),
                           (columanXActual - 1, filaYActual + 1),
                           (columanXActual + 1, filaYActual - 1)]

                if self.puedoExplorarAlgunaCasilla(vecinos) or self.puedoExplorarCasilla((columanXActual, filaYActual)):
                    seguir = False

                    if self.mePuedoMoverSinDarSaltos(columanXActual, filaYActual):
                        self.coordenadas = (columanXActual, filaYActual)
                        self.mapaLocal[filaYActual][columanXActual].tipo = TipoCasilla.VISITADO
                        self.mapaGlobal[filaYActual][columanXActual].tipo = TipoCasilla.VISITADO
                    else:
                        self.rutaAEstrella = astar(self.coordenadas, (columanXActual, filaYActual), self.mapaGlobal)
                        self.siguiendoAEstrella = True

                    for columnaXVecina, filaYVecina in vecinos:
                        if self.puedoExplorarCasilla((columnaXVecina, filaYVecina)):
                            self.colaBFS.append((columnaXVecina, filaYVecina))

            return True

    def puedoExplorarAlgunaCasilla(self, coordenadasCasillas: List[Tuple[int, int]]) -> bool:
        for coordenadaCasilla in coordenadasCasillas:
            if self.puedoExplorarCasilla(coordenadaCasilla):
                return True

        return False

    def puedoExplorarCasilla(self, coordenadaCasilla: Tuple[int, int]) -> bool:
        maxY, maxX = self.alto, self.ancho
        x, y = coordenadaCasilla

        dentroDeLosLimites = 0 <= x < maxX and 0 <= y < maxY
        noHayPared = self.mapaGlobal[y][x].tipo is TipoCasilla.NADA
        noLoHeVisitado = self.mapaLocal[y][x].tipo is not TipoCasilla.VISITADO

        return dentroDeLosLimites and noHayPared and noLoHeVisitado

    def mePuedoMoverSinDarSaltos(self, nuevaX, nuevaY):
        difX = abs(self.coordenadas[0] - nuevaX)
        difY = abs(self.coordenadas[1] - nuevaY)

        return difY < 2 and difX < 2

    # def quitar_niebla(self):
    #     robot_x, robot_y = self.coordenadas
    #     for i in range(max(0, robot_x - self.VIEWPORT_RADIUS), min(self.alto, robot_x + self.VIEWPORT_RADIUS + 1)):
    #         for j in range(max(0, robot_y - self.VIEWPORT_RADIUS), min(self.ancho, robot_y + self.VIEWPORT_RADIUS + 1)):
    #             distance = np.sqrt((i - robot_x) ** 2 + (j - robot_y) ** 2)
    #             if distance <= self.VIEWPORT_RADIUS:
    #                 self.niebla[i][j].tipo = self.mapaGlobal[i][j].tipo
