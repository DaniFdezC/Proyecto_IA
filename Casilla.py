from enum import Enum

class TipoCasilla(Enum):
    NADA = 0
    PARED = 1
    VISITADO = 2
    OBJETIVO = 3
    NIEBLA = 4
    ROBOT = 5
    VICTIMA = 6
    RESCATADO = 7

class TipoObjetivo(Enum):
    NADA = 0,
    LIBRE = 1,
    CAPTURADO = 2

class Casilla:
    def __init__(self, tipo=TipoCasilla.NADA, tipoObjetivo=TipoObjetivo.NADA):
        self.tipo = tipo
        self.tipoObjetivo = tipoObjetivo