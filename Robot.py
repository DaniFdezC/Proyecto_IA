from enum import Enum
from Casilla import *
from Algoritmo import *

class TipoEstado(Enum):
    BUSCANDO = 0
    AESTRELLA = 1

class Robot:
    def __int__(self, mapaGlobal, coordenadas, campoVision):
        self.mapaGlobal = mapaGlobal
        self.coordenadas = coordenadas
        self.mapaLocal = None
        self.estado = TipoEstado.BUSCANDO
        self.objetivoFinal = None
        self.campoVision = campoVision
        self.rutaDefinida = None
        self.ultimoPuntoPosibleAlgoritmo = UltimoPuntoPosible()

    def moverse(self):
        robotCerca = self.getRobotCerca()
        if robotCerca is not None:
            self.mapaLocal.MezclarMapa(robotCerca.mapaLocal)

        ## Si hay objetivoFinal ni ruta definida, busca camino con A*
        if self.objetivoFinal is not None and self.rutaDefinida is not None:
            self.hazEstrella()

        ## Si hay objetivoFinal y tiene ruta, que se vaya moviendo hacia el objetivo
        elif self.coordenadas is not self.objetivoFinal:
            self.seguirRuta()

        elif self.coordenadas is self.objetivoFinal:
            self.resetearObjetivoFinal()

        else:
            self.explorar()


    def explorar(self):
        objetivoAlrededor = self.getObjetivoAlrededorDisponible()

        if objetivoAlrededor is not None:
            self.objetivoFinal = objetivoAlrededor

        else:
            self.explorarCasillasDesconocidas()

    def explorarCasillasDesconocidas(self):
         self.ultimoPuntoPosibleAlgoritmo.getSiguienteMovimiento()
    def getRobotCerca(self):
        for posicionCampoVision in self.campoVision:
            casilla = self.mapaGlobal.GetCasilla((posicionCampoVision[0] + self.coordenadas.x, posicionCampoVision[1] + self.coordenadas.y))
            if casilla.robotContenedor is not None:
                return casilla.robotContenedor
        return None

    def getObjetivoAlrededorDisponible(self):
        for posicionCampoVision in self.campoVision:
            casilla = self.mapaGlobal.GetCasilla((posicionCampoVision[0] + self.coordenadas.x, posicionCampoVision[1] + self.coordenadas.y))
            if not casilla.estaCogida and casilla.tipo is TipoCasilla.OBJETIVO:
                return casilla
        return None

    def seguirRuta(self):
        ruta = self.rutaDefinida.pop()
        self.coordenadas = ruta

    def resetearObjetivoFinal(self):
        self.objetivoFinal = None
        self.rutaDefinida = None

    def hazEstrella(self):
        ruta = RealizaAEstrella(self.mapaGlobal, self.coordenadas, self.objetivoFinal)
        if ruta is not None:
            self.rutaDefinida = ruta

