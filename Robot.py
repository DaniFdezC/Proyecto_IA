from enum import Enum
from Casilla import *
from Algoritmo import *
from collections import deque
import numpy as np
from Aestrella import *
from typing import *
from queue import Queue


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
        self.indiceRuta = 0

        self.objetivos = []
        self.objetivoMarcado = None
        self.rutaAlObjetivo = False

    def moverse(self):

        if self.objetivoMarcado == self.coordenadas:
            # print("Dejo de seguir al objetivo")
            self.objetivoMarcado = None
            self.siguiendoAEstrella = False

        self.comprobarSiPuedoIrAObjetivo()

        if self.siguiendoAEstrella is False:
            seguir = True

            while seguir:
                if not self.colaBFS:
                    return False

                columanXActual, filaYActual = self.colaBFS.pop()

                vecinos = self._getVecinos(columanXActual, filaYActual)

                if self._puedoExplorarAlgunaCasilla(vecinos) or self._puedoExplorarCasilla((columanXActual, filaYActual)):
                    seguir = False

                    self.comprobarSiPuedoIrAObjetivo()

                    if self._mePuedoMoverSinDarSaltos(columanXActual, filaYActual):
                        self.coordenadas = (columanXActual, filaYActual)
                        self._marcarVisitadas(self.coordenadas)

                        radioVision = self.radioVision((filaYActual, columanXActual))

                        for filaVision, columnaVision in radioVision:

                            if self._puedoExplorarCasilla((columnaVision, filaVision)):
                                self.mapaLocal[filaVision][columnaVision].tipo = TipoCasilla.VISIONADA
                                self.mapaGlobal[filaVision][columnaVision].tipo = TipoCasilla.VISIONADA
                                if self.mapaGlobal[filaVision][columnaVision].tipoObjetivo == TipoObjetivo.LIBRE:
                                    if (filaVision, columnaVision) not in self.objetivos and (
                                            filaVision, columnaVision) != self.objetivoMarcado:
                                        self.objetivos.append((filaVision, columnaVision))

                        for columnaXVecina, filaYVecina in vecinos:
                            coordenadaVecina = (columnaXVecina, filaYVecina)

                            if self._puedoExplorarCasilla(
                                    coordenadaVecina) and coordenadaVecina not in self.colaBFS:

                                self.colaBFS.append(coordenadaVecina)
                                if self._esVecino(coordenadaVecina):
                                    self.mapaLocal[filaYVecina][columnaXVecina].tipo = TipoCasilla.VISITADO
                                    self.mapaGlobal[filaYVecina][columnaXVecina].tipo = TipoCasilla.VISITADO

                    else:
                        self.rutaAEstrella = astar(self.coordenadas, (columanXActual, filaYActual), self.mapaGlobal)
                        self.siguiendoAEstrella = True

        if self.siguiendoAEstrella:
            self.coordenadas = self.rutaAEstrella[self.indiceRuta]
            self._marcarVisitadas(self.coordenadas)
            self.indiceRuta += 1

            if self.indiceRuta >= len(self.rutaAEstrella):
                self.siguiendoAEstrella = False
                self.indiceRuta = 0

            columnaActual, filaActual = self.coordenadas

            radioVision = self.radioVision((filaActual, columnaActual))

            for filaVision, columnaVision in radioVision:

                if self._puedoExplorarCasilla((columnaVision, filaVision)):
                    self.mapaLocal[filaVision][columnaVision].tipo = TipoCasilla.VISIONADA
                    self.mapaGlobal[filaVision][columnaVision].tipo = TipoCasilla.VISIONADA
                    if self.mapaGlobal[filaVision][columnaVision].tipoObjetivo == TipoObjetivo.LIBRE:
                        if (filaVision, columnaVision) not in self.objetivos and (
                                filaVision, columnaVision) != self.objetivoMarcado:
                            self.objetivos.append((filaVision, columnaVision))

            vecinos = self._getVecinos(columnaActual, filaActual)

            for columnaXVecina, filaYVecina in vecinos:
                coordenadaVecina = (columnaXVecina, filaYVecina)

                if self._puedoExplorarCasilla(
                        coordenadaVecina) and coordenadaVecina not in self.colaBFS:

                    self.colaBFS.append(coordenadaVecina)
                    if self._esVecino(coordenadaVecina):
                        self.mapaLocal[filaYVecina][columnaXVecina].tipo = TipoCasilla.VISITADO
                        self.mapaGlobal[filaYVecina][columnaXVecina].tipo = TipoCasilla.VISITADO

        return True


    def comprobarSiPuedoIrAObjetivo(self):
        if len(self.objetivos) > 0 and self.objetivoMarcado is None:
            for objetivo in self.objetivos:
                filaObjetivo, columnaObjetivo = objetivo
                self.rutaAlObjetivo = astar(self.coordenadas, (columnaObjetivo, filaObjetivo), self.mapaLocal)
                if self.rutaAlObjetivo != False:
                    # print("Empiezo a seguir al objetivo")
                    self.rutaAEstrella = self.rutaAlObjetivo
                    self.objetivoMarcado = (columnaObjetivo, filaObjetivo)
                    self.siguiendoAEstrella = True
                    self.objetivos.remove(objetivo)
                    self.indiceRuta = 0
    def intercambiarMapa(self, otroRobot, darLaVueltaCola: bool):
        self._mezclarMapaLocales(otroRobot)
        self._borrarElementosPilaBFS(darLaVueltaCola)

    def _mezclarMapaLocales(self, otroRobot):
        for otroRobotMapaLocalY in range(len(otroRobot.mapaLocal)):
            for otroRobotMapaLocalX in range(len(otroRobot.mapaLocal[otroRobotMapaLocalY])):
                self.mapaLocal[otroRobotMapaLocalY][otroRobotMapaLocalX] = otroRobot.mapaLocal[otroRobotMapaLocalY][otroRobotMapaLocalX]

    def _borrarElementosPilaBFS(self, darLaVueltaColaBfs: bool):
        numeroElementosBorrados = 0

        for indiceCoordenadaBfs, coordenadaBfs in enumerate(list(self.colaBFS)):
            vecinos = self._getVecinos(coordenadaBfs[0], coordenadaBfs[1])
            if not self._puedoExplorarAlgunaCasilla(vecinos) and not self._puedoExplorarCasilla(coordenadaBfs):
                del self.colaBFS[indiceCoordenadaBfs - numeroElementosBorrados]
                numeroElementosBorrados += 1

        if darLaVueltaColaBfs:
            self.colaBFS.reverse()

    def _puedoExplorarAlgunaCasilla(self, coordenadasCasillas: List[Tuple[int, int]]) -> bool:
        for coordenadaCasilla in coordenadasCasillas:
            if self._puedoExplorarCasilla(coordenadaCasilla):
                return True

        return False

    def _puedoExplorarCasilla(self, coordenadaCasilla: Tuple[int, int]) -> bool:
        x, y = coordenadaCasilla

        noLoHeVisitado = self.mapaLocal[y][x].tipo is not TipoCasilla.VISITADO
        noHayPared = self.mapaGlobal[y][x].tipo is not TipoCasilla.PARED
        dentroDeLosLimites = self._dentroDeLosLimites(x, y)

        return dentroDeLosLimites and noHayPared and noLoHeVisitado

    def _mePuedoMoverSinDarSaltos(self, nuevaX, nuevaY):
        difX = abs(self.coordenadas[0] - nuevaX)
        difY = abs(self.coordenadas[1] - nuevaY)

        return difY < 2 and difX < 2

    def _marcarVisitadas(self, coordenadas: Tuple[int, int]):
        x, y = coordenadas
        self.mapaLocal[y][x].tipo = TipoCasilla.VISITADO
        self.mapaGlobal[y][x].tipo = TipoCasilla.VISITADO

    def _esVecino(self, coordenadas: Tuple[int, int]) -> bool:
        return coordenadas in self._getVecinos(self.coordenadas[0], self.coordenadas[1])

    def _dentroDeLosLimites(self, x: int, y: int) -> bool:
        maxY, maxX = self.alto, self.ancho
        return 0 <= x < maxX and 0 <= y < maxY

    def _getVecinos(self, x: int, y: int) -> List[Tuple[int, int]]:
        return [(x - 1, y),
                (x, y + 1),
                (x + 1, y),
                (x, y - 1),
                (x - 1, y - 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x + 1, y + 1)]


    def radioVision(self, coordenadaVision):
        campoVision = []

        for fila, columna in self.campoVision:
            new_row = coordenadaVision[0] + fila
            new_col = coordenadaVision[1] + columna

            if 0 <= new_row < self.alto and 0 <= new_col < self.ancho and self.mapaGlobal[new_row][new_col].tipo is not TipoCasilla.PARED:
                campoVision.append((new_row, new_col))

        return campoVision

    # def quitar_niebla(self):
    #     robot_x, robot_y = self.coordenadas
    #     for i in range(max(0, robot_x - self.VIEWPORT_RADIUS), min(self.alto, robot_x + self.VIEWPORT_RADIUS + 1)):
    #         for j in range(max(0, robot_y - self.VIEWPORT_RADIUS), min(self.ancho, robot_y + self.VIEWPORT_RADIUS + 1)):
    #             distance = np.sqrt((i - robot_x) ** 2 + (j - robot_y) ** 2)
    #             if distance <= self.VIEWPORT_RADIUS:
    #                 self.niebla[i][j].tipo = self.mapaGlobal[i][j].tipo
