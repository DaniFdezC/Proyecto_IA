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
        self.coordenadasIniciales = coordenadas

        self.alto = len(mapaGlobal)
        self.ancho = len(mapaGlobal[0])

        self.mapaLocal =[[Casilla() for _ in range(self.ancho)] for _ in range(self.alto)]
        self.colaBFS = deque([coordenadas])
        self.siguiendoAEstrella = False
        self.rutaAEstrella = None
        self.indiceRuta = 1

    """def moverse(self):
        if self.siguiendoAEstrella:
            self.coordenadas = self.rutaAEstrella[self.indiceRuta]
            self.indiceRuta += 1
            if len(self.rutaAEstrella) >= self.indiceRuta:
                self.siguiendoAEstrella = False
                self.indiceRuta = 1

        if self.siguiendoAEstrella is False:
            if not self.colaBFS:
                return False

            # Ir haciendo pop hasta que encontremos uno que almenos 1 vecino no este visitado.
            filaActual, columnaActual = self.colaBFS.pop()
            vecinos = [(filaActual - 1, columnaActual), (filaActual + 1, columnaActual),
                         (filaActual, columnaActual - 1), (filaActual, columnaActual + 1),
                         (filaActual - 1, columnaActual - 1), (filaActual + 1, columnaActual + 1),
                         (filaActual - 1, columnaActual +1), (filaActual + 1, columnaActual -1)]

            if self.mePuedoMoverSinDarSaltos(filaActual, columnaActual):
                self.coordenadas = (filaActual, columnaActual)
            else:
                self.rutaAEstrella = astar(self.coordenadas, (filaActual, columnaActual), self.mapaLocal)
                self.siguiendoAEstrella = True


            for continuefilaVecina, columnaVecina in vecinos:
                if self.mePuedoMover(filaVecina, columnaVecina):
                    self.colaBFS.append((filaVecina, columnaVecina))

                    self.mapaLocal[filaVecina][columnaVecina].tipo = TipoCasilla.VISITADO
                    self.mapaGlobal[filaVecina][columnaVecina].tipo = TipoCasilla.VISITADO
                    self.quitar_niebla()

            return True"""

    def moverse2(self):
        if self.siguiendoAEstrella:
            self.coordenadas = self.rutaAEstrella[self.indiceRuta]
            self.indiceRuta += 1
            if len(self.rutaAEstrella) >= self.indiceRuta:
                self.siguiendoAEstrella = False
                self.indiceRuta = 1

        if self.siguiendoAEstrella is False:
            seguir = True

            while seguir:
                if not self.colaBFS:
                    return False
                filaActual, columnaActual = self.colaBFS.pop()
                #print(len(self.colaBFS))
                vecinos = [(filaActual - 1, columnaActual), (filaActual + 1, columnaActual),
                             (filaActual, columnaActual - 1), (filaActual, columnaActual + 1),
                             (filaActual - 1, columnaActual - 1), (filaActual + 1, columnaActual + 1),
                             (filaActual - 1, columnaActual + 1), (filaActual + 1, columnaActual - 1)]

                if not self.algunaCasillaNoVisitada(vecinos):
                    seguir = True
                else:
                    if self.mePuedoMoverSinDarSaltos(filaActual, columnaActual):
                        self.coordenadas = (filaActual, columnaActual)


                    else:
                        self.rutaAEstrella = astar(self.coordenadas, (filaActual, columnaActual), self.mapaLocal)
                        self.siguiendoAEstrella = True

                    seguir = False

                for filaVecina, columnaVecina in vecinos:
                    if self.mePuedoMover(filaVecina, columnaVecina):
                        self.colaBFS.append((filaVecina, columnaVecina))

                        self.mapaLocal[filaVecina][columnaVecina].tipo = TipoCasilla.VISITADO
                        self.mapaGlobal[filaVecina][columnaVecina].tipo = TipoCasilla.VISITADO
                        self.quitar_niebla()

            return True


    def todasLasCasillasVisitadas(self, casillas):
        for casilla in casillas:
            if self.mapaLocal[casilla[0]][casilla[1]].tipo is not TipoCasilla.VISITADO:
                return False

        return True

    def algunaCasillaNoVisitada(self, casillas):
        for casilla in casillas:
            if self.mapaLocal[casilla[0]][casilla[1]].tipo is TipoCasilla.NADA:
                return True

        return False

    def mePuedoMoverSinDarSaltos(self, nuevaX, nuevaY):
        difX = abs(self.coordenadas[0] - nuevaX)
        difY = abs(self.coordenadas[1] - nuevaY)

        return difY < 2 and difX < 2



    def mePuedoMover(self, row, col):
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
