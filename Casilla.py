from enum import Enum

class TipoCasilla(Enum):
    NADA = 0
    PARED = 1
    DESCONOCIDO = 2
    OBJETIVO = 3

class Casilla:
    def __init__(self, estaCogida=False, tipo=TipoCasilla.NADA, robotContenedor=None):
        self.estaCogida = estaCogida
        self.tipo = tipo
        self.robotContenedor = robotContenedor