from enum import Enum

from enum import Enum

class TipoCasilla(Enum):
    NADA = 0
    PARED = 1
    NIEBLA = 4
    ROBOT = 5
    VICTIMA = 6
    RESCATADO = 7

class Casilla:
    def __init__(self, tipo=TipoCasilla.NADA):
        self.tipo = tipo
