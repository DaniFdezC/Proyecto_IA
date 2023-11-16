from enum import Enum

class TipoCasilla(Enum):
    NADA = 0
    PARED = 1
    VISITADO = 2
    OBJETIVO = 3
    NIEBLA = 4

class Casilla:
    def __init__(self, tipo=TipoCasilla.NADA):
        self.tipo = tipo